import Data_process
import path_define as PreDefine


class Load_Batch:

    def __init__(self):
        # linear_regression X and Y
        self.linear_regression_X,self.linear_regression_Y = Data_process.linear_regression_initial()

    # def get_batch(self,data_x,data_y,batch_size):
    #     # 生成batch
    #     start = 0
    #     end = batch_size
    #
    #     batch_num = len(data_x)//batch_size
    #
    #     for _ in range(batch_num):
    #
    #         batch_inputs = data_x[start:end]
    #         batch_target = data_y[start:end]
    #
    #         yield batch_inputs, batch_target
    #         start += batch_size
    #         end += batch_size

    def get_batch(self,data_x,data_y,batch_size,item):
        # 生成batch

        if item == PreDefine.Model_mode[0]:
            start = 0
            end = batch_size
            batch_num = 5
        else:
            start = 5*batch_size
            end = start+batch_size
            batch_num = 2

        for _ in range(batch_num):

            batch_inputs = data_x[start:end]
            batch_target = data_y[start:end]

            yield batch_inputs, batch_target
            start += batch_size
            end += batch_size


if __name__ == "__main__":

    batch = Load_Batch()

    for i,j in batch.linear_regression_Batches:
        print(i)
        print(j)
