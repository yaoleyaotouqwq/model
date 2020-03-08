import pandas as pd
import path_define as PreDefine
import Data
from sklearn import preprocessing

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


def linear_regression_initial():
    """
    对初始数据进行加工处理
    :return:
    """
    # 不把第一行当属性
    initial_data = pd.read_csv(PreDefine.initial_data_path,header=None).values

    x_data = []
    y_data = []

    # x 和 y分离,把评分等级换算成分数
    for temp in initial_data:
        x_data.append(list(temp[:8]) + list(temp[9:20]) + [Data.Score_dict[temp[20]]]+list(temp[21:]))
        y_data.append(temp[8])

    # 将数据缩至0-1之间
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaler_data = min_max_scaler.fit_transform(x_data)

    # 分数one_hot准备
    onehot_temp = [0 for temp in range(Data.Score_scope_len)]
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

    # print(x_scaler_data)
    # print(y_onehot_data)

    return x_scaler_data,y_onehot_data


if __name__ == '__main__':
    linear_regression_initial()