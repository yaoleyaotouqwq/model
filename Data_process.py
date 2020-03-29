import Data
from sklearn import preprocessing
from sklearn.preprocessing import minmax_scale

# 打印隐藏元素
# from numpy import *
# set_printoptions(threshold=NaN)


def binary_find(data,left,right,values):
    """
    二分查找
    """
    index = (left+right)//2

    if index >= 0 or index < right - 1:
        if (values - data[index]) * (values - data[index+1]) < 0:
            return index
        elif values - data[index] == 0:
            return index
        elif values - data[index+1] == 0:
            return index+1
        elif (values - data[index]) + (values - data[index+1]) > 0:
            return binary_find(data, index+1 , right , values)
        elif (values - data[index]) + (values - data[index+1]) < 0:
            return binary_find(data, left , index , values)
    else:
        return -1


def data_process(data):
    x_data = []
    y_data = []

    # 判断传进来是一纬还是二纬list
    if isinstance(data[0], list):
        # x 和 y分离,把评分等级换算成分数
        for temp in data:
            temp_x = list(temp[:8]) + list(temp[9:20]) + [Data.Score_dict[temp[20]]]+list(temp[21:])
            temp_y = [temp[8]]

            x_data.append([0. if values is "" else float(values) for values in temp_x])
            y_data.append([0. if values is "" else float(values) for values in temp_y][0])

        # 将数据缩至0-1之间
        x_scaler_data = minmax_scale(x_data, axis=0)
    else:
        temp_x = list(data[:8]) + list(data[9:20]) + [Data.Score_dict[data[20]]] + list(data[21:])
        temp_y = [data[8]]

        x_data.append([0. if temp is "" else float(temp) for temp in temp_x])
        y_data = [0. if temp is "" else float(temp) for temp in temp_y]

        # 将数据缩至0-1之间
        x_scaler_data = minmax_scale(x_data,axis=1)

    # 分数one_hot准备,在模型的softmax多分类的过程中，
    y_onehot_list = []
    data_scope = Data.Score_scope
    data_scope_len = Data.Score_scope_len

    # 寻找成绩所在区间
    for temp in y_data:
        index = binary_find(data_scope,0,data_scope_len,temp)
        y_onehot_list.append([index])

    # sklearn方法转换成onehot数据
    enc = preprocessing.OneHotEncoder(sparse = False,n_values = [data_scope_len])
    y_onehot_data = enc.fit_transform(y_onehot_list)

    return x_scaler_data,y_onehot_data
