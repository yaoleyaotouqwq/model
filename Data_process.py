import pandas as pd
import os

def initial_process():
    """
    对初始数据进行加工处理
    :return:
    """
    print(os.getcwd())
    initial_data = pd.read_csv('initial_data.csv').values
    print(initial_data)
    exit()

def linear_regression_batch():
    """
    产生线性回归所需数据的batch
    :return:
    """
    pass


if __name__ == "__main__":
    initial_process()
