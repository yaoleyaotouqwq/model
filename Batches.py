import Data_process

class Load_Batch:

    def __init__(self,score_data):
        # original data for X and Y
        self.Data_X,self.Data_Y = Data_process.data_process(score_data)

    def get_batch(self,data_x,data_y,batch_size):
        # 生成batch
        start = 0
        end = batch_size

        batch_num = len(data_x)//batch_size

        for _ in range(batch_num):

            batch_inputs = data_x[start:end]
            batch_target = data_y[start:end]

            yield batch_inputs, batch_target
            start += batch_size
            end += batch_size

    # def get_batch(self,data_x,data_y,batch_size,item):
    #     # 生成batch
    #
    #     if item == PreDefine.Model_mode[0]:
    #         start = 0
    #         end = batch_size
    #         batch_num = PreDefine.Batch_num1['logistics_regression']
    #     else:
    #         start = PreDefine.Batch_num1['logistics_regression']*batch_size
    #         end = start+batch_size
    #         batch_num = PreDefine.Batch_num2['logistics_regression']
    #
    #     for _ in range(batch_num):
    #
    #         batch_inputs = data_x[start:end]
    #         batch_target = data_y[start:end]
    #
    #         yield batch_inputs, batch_target
    #         start += batch_size
    #         end += batch_size

