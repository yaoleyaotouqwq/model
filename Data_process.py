import Data
from sklearn import preprocessing
from sklearn.preprocessing import minmax_scale
from sklearn.model_selection import KFold
import path_define as PreDefine

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

    # 标记数据是否为dict，是否处于评估态
    is_dict = False
    if isinstance(data,dict):
        is_dict = True
        use_data = data['data']
        for temp in use_data:
            temp_x = list(temp[:8]) + list(temp[9:20]) + [Data.Score_dict[temp[20]]] + list(temp[21:])
            temp_y = [temp[8]]

            x_data.append([0. if values is "" else float(values) for values in temp_x])
            y_data.append([0. if values is "" else float(values) for values in temp_y][0])

        # 开始选择划分的数据来做评估
        sfolder = KFold(n_splits=PreDefine.Test_K_num, shuffle=False)
        # 用来判断划分序号
        times = 0
        # 细分数据集
        train_data_x = []
        train_data_y = []
        test_data_x = []
        test_data_y = []

        for train_list, test_list in sfolder.split(x_data, y_data):
            if times == data['times']:
                for temp1 in train_list:
                    train_data_x.append(x_data[temp1])
                    train_data_y.append(y_data[temp1])
                for temp2 in test_list:
                    test_data_x.append(x_data[temp2])
                    test_data_y.append(y_data[temp2])
            times+=1

        # 将数据缩至0-1之间
        x_scaler_data = {
            "train_x_scaler_data":minmax_scale(train_data_x, axis=0),
            "test_x_scaler_data":minmax_scale(test_data_x, axis=0)
        }

    else:
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

    data_scope = Data.Score_scope
    data_scope_len = Data.Score_scope_len

    # sklearn方法转换成onehot数据
    enc = preprocessing.OneHotEncoder(sparse=False, n_values=[data_scope_len])

    # 分数one_hot准备,用于模型的softmax多分类
    if not is_dict:
        y_onehot_list = []
        # 寻找成绩所在区间
        for temp in y_data:
            index = binary_find(data_scope, 0, data_scope_len, temp)
            y_onehot_list.append([index])

        y_onehot_data = enc.fit_transform(y_onehot_list)
    else:
        train_y_onehot_list = []
        test_y_onehot_list = []
        # 寻找成绩所在区间
        for temp in train_data_y:
            index = binary_find(data_scope, 0, data_scope_len, temp)
            train_y_onehot_list.append([index])

        for temp in test_data_y:
            index = binary_find(data_scope, 0, data_scope_len, temp)
            test_y_onehot_list.append([index])

        y_onehot_data = {
            "train_y_onehot_list":enc.fit_transform(train_y_onehot_list),
            "test_y_onehot_list": enc.fit_transform(test_y_onehot_list)
        }

    return x_scaler_data,y_onehot_data
