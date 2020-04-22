import tensorflow as tf
import pickle as pk
import GUI_Parameter as Parameter
import path_define as PreDefine
import Data_process as data_process
import Batches
import os
import numpy as np

class LR:
    def __init__(self):

        self.Graph = tf.Graph()
        with self.Graph.as_default():
            self.X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["LR"])
            self.Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["LR"])
            self.W = tf.Variable(
                tf.truncated_normal(shape=PreDefine.W_shape["LR"], stddev=PreDefine.Normal_variable))
            self.B = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["LR"]))

            # with tf.name_scope("Result"):
            # 采用softmax实现逻辑回归的多分类
            self.Result = tf.nn.softmax(tf.matmul(self.X, self.W) + self.B)
            # with tf.name_scope("Loss"):
            self.Loss = tf.reduce_mean(tf.reduce_sum(-self.Y*tf.log(self.Result), reduction_indices=1))
            # with tf.name_scope("Train_op"):
            self.Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["LR"]).minimize(self.Loss)
            # with tf.name_scope("Accuracy"):
            self.Acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(self.Y, 1), tf.argmax(self.Result, 1)), 'float'))
        # 用来显示标量信息
        # tf.summary.scalar("loss", self.Loss)
        # tf.summary.scalar("accuracy", self.Acc)

    # 评估统计
    def test_ACC(self,test_data,low_score):
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()
            Batch = Batches.Load_Batch(test_data)

            # 将数据细分出来
            train_x = Batch.Data_X['train_x_scaler_data']
            train_y = Batch.Data_Y['train_y_onehot_list']
            test_x = Batch.Data_X['test_x_scaler_data']
            test_y = Batch.Data_Y['test_y_onehot_list']

            loss = 0
            acc = 0

            for step in range(PreDefine.Train_step["LR"]):
                batches = Batch.get_batch(train_x, train_y,
                                          PreDefine.Batch_size["LR"])
                batch_times = 0
                for data_x,data_y in batches:

                    feed = {
                        self.X: data_x,
                        self.Y: data_y
                    }

                    _,loss = self.sess.run([self.Train_op,self.Loss], feed_dict=feed)
                    batch_times+=1

                if step % 20 == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    print("step %d , Loss is %f , Acc is %f" % (step,loss,acc))

            acc = self.Acc.eval(feed_dict={self.X:test_x,self.Y:test_y})
            print("LR model the number {0} test score is {1}".format(
                test_data['times']+1,acc))

            # 记录每个模型评估准确率
            new_score = acc

            if new_score >= low_score:
                low_score = new_score
                # 保存训练的模型，low_score用来保存最优模型
                Saver = tf.train.Saver()
                Saver.save(self.sess,PreDefine.Model_path2["LR"]+'/LR',global_step=step)

        return low_score,new_score

        # 评估主控函数
    def LR_test(self,data):

        # 重新训练
        # 清空原训练模型文件
        if os.path.exists(PreDefine.Model_path1['LR']):
            for file in os.listdir(PreDefine.Model_path1['LR']):
                os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['LR'] + file))

        Test_data = {
            "data":data,
            "times":0
        }
        # 区分第几折数据
        times =  0
        # 设立一个最低分,默认-100
        low_score = -100

        # 评估算法的表现
        acc_score = 0

        # 传递数据画图
        times_list = []
        new_score_list = []
        average_score_list = []

        for temp in range(PreDefine.Test_K_num):
            Test_data["times"] = times
            # new_score为每个模型的分数
            low_score,new_score = self.test_ACC(Test_data,low_score)
            times+=1
            acc_score+=new_score

            times_list.append(str(times))
            new_score_list.append(new_score*100)
            average_score_list.append(acc_score/PreDefine.Test_K_num)
            yield times_list,new_score_list,average_score_list

    def LR_prediction(self,score_data):
        # 记录预测结果
        result = []
        truly = []
        # 模型预测
        # 加载训练的模型
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            Saver = tf.train.Saver()
            # 恢复模型
            Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["LR"]))
            x_data, y_data = data_process.data_process(score_data)

            data_len = len(x_data)

            for i in range(data_len):
                feed = {
                    self.X: [x_data[i]],
                    self.Y: [y_data[i]]
                }
                print(self.sess.run(self.Result, feed_dict=feed))
                result.append(np.argmax(self.sess.run(self.Result, feed_dict=feed)))
                truly.append(np.argmax(y_data[i]))

        return [result,truly]

    def LR_train(self,model_mode,score_data):

        # 保存训练结果
        step_list = []
        loss_list = []
        acc_list = []

        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            # 保存训练的模型
            Saver = tf.train.Saver()

            # 将所有summary全部保存到磁盘，以便tensorboard显示
            # self.Merged_summary_op = tf.summary.merge_all()

            # 指定一个文件用来保存图。tf.get_default_graph()可以获取当前默认的计算图
            # summary_writer = tf.summary.FileWriter(PreDefine.tensorBoard_path['LR'],
            #                                        graph=tf.get_default_graph())

            # 初次或重新训练
            if model_mode == PreDefine.Model_mode[0]:
                # 清空原训练模型文件
                if os.path.exists(PreDefine.Model_path1['LR']):
                    for file in os.listdir(PreDefine.Model_path1['LR']):
                        os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['LR'] + file))

            else:
                # 恢复模型继续训练
                Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["LR"]))

            Batch = Batches.Load_Batch(score_data)

            for step in range(PreDefine.Train_step["LR"]):
                batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                          PreDefine.Batch_size["LR"])
                batch_times = 0
                for data_x,data_y in batches:

                    feed = {
                        self.X: data_x,
                        self.Y: data_y
                    }

                    # _,merged_summary_op,loss = self.sess.run([self.Train_op,self.Merged_summary_op,self.Loss], feed_dict=feed)
                    _,loss = self.sess.run([self.Train_op,self.Loss], feed_dict=feed)

                    # 将训练过程数据保存在filewriter指定的文件中
                    # if model_mode == PreDefine.Model_mode[0]:
                    #     summary_writer.add_summary(merged_summary_op, step*PreDefine.Batch_num1['LR']+batch_times)
                    # else:
                    #     summary_writer.add_summary(merged_summary_op, step*PreDefine.Batch_num2['LR']+batch_times)

                    batch_times+=1

                if step % 20 == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    print("step %d , Loss is %f , Acc is %f" % (step,loss,acc))

                if step % Parameter.Model_Refresh_num == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    step_list.append(str(step))
                    loss_list.append(loss)
                    acc_list.append(acc*100)

                    yield step_list, loss_list, acc_list

            print("Train acc is "+ str(self.Acc.eval(feed_dict={self.X:Batch.Data_X,self.Y:Batch.Data_Y})))
            Saver.save(self.sess,PreDefine.Model_path2["LR"]+'/LR',global_step=step)


class SVM:

    def __init__(self):
        self.Graph = tf.Graph()
        with self.Graph.as_default():
            self.X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["SVM"])
            self.Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["SVM"])
            self.Prediction_gird = tf.placeholder(shape=PreDefine.SVM_prediction_gird_shape,dtype=tf.float32)
            self.B = tf.Variable(tf.truncated_normal(shape=PreDefine.B_shape["SVM"], stddev=PreDefine.Normal_variable))

            # 径向基函数（RBF）,将线性不可分问题转化到高纬度的线性可分
            # 公式为k = exp{- ||x-xc||^2/(2*σ^2) }
            # 缩放比例,通常取值0.01、0.1、1、10、100，相当于公式的 -1/2*σ^2
            self.Gamma = tf.constant(PreDefine.RBF["Gamma"])
            self.Dist = tf.reshape(tf.reduce_sum(tf.square(self.X),1),[-1,1])
            self.Norm = tf.add(
                tf.subtract(
                    self.Dist,
                    tf.multiply(2.,tf.matmul(self.X,tf.transpose(self.X)))
                ),
                tf.transpose(self.Dist)
            )
            self.Kernel = tf.exp(tf.multiply(self.Gamma,tf.abs(self.Norm)))

            # 对偶问题Loss = −∑(∑b−∑(K*||b||^2 *||y||^2))
            self.Loss = tf.reduce_sum(
                tf.negative(
                    tf.subtract(
                        tf.reduce_sum(self.B),
                            tf.reduce_sum(
                                tf.multiply(
                                    self.Kernel,
                                    tf.multiply(
                                        tf.matmul(tf.transpose(self.B),self.B),
                                        self.reshape_matmul(self.Y)
                                    )
                                ),[1, 2]
                            )
                        )
                    )
                )

            self.Predict_kernal = tf.exp(
                tf.multiply(
                    self.Gamma,
                    tf.abs(
                        tf.add(
                            tf.subtract(
                                tf.reshape(tf.reduce_sum(tf.square(self.X),1),[-1,1]),
                                tf.multiply(2.,tf.matmul(self.X,tf.transpose(self.Prediction_gird)))
                            ),
                            tf.transpose(tf.reshape(tf.reduce_sum(tf.square(self.Prediction_gird),1),[-1,1]))
                        )
                    )
                )
            )

            self.Predict_output = tf.matmul(tf.multiply(self.Y, self.B), self.Predict_kernal)
            # 平均值，tf.expand_dims增加一维
            self.Predict_result = tf.argmax(self.Predict_output - tf.expand_dims(tf.reduce_mean(self.Predict_output, 1), 1), 0)
            # 训练准确率
            self.Predict_ACC = tf.reduce_mean(tf.cast(tf.equal(self.Predict_result, tf.argmax(self.Y, 0)), tf.float32))

            # 梯度下降优化
            self.Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["SVM"]).minimize(self.Loss)

    def reshape_matmul(self, data):
        data1 = tf.expand_dims(data, 1)
        data2 = tf.reshape(data1, [PreDefine.Class_num, PreDefine.Batch_size["SVM"], 1])
        return tf.matmul(data2, data1)

    # 评估统计
    def test_ACC(self, test_data, low_score):
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()
            Batch = Batches.Load_Batch(test_data)

            # 将数据细分出来
            train_x = Batch.Data_X['train_x_scaler_data']
            train_y = Batch.Data_Y['train_y_onehot_list']
            test_x = Batch.Data_X['test_x_scaler_data']
            test_y = Batch.Data_Y['test_y_onehot_list']

            loss = 0
            acc = 0
            # 记录最低训练分
            low_acc = 0

            for step in range(PreDefine.Train_step["SVM"]):
                batches = Batch.get_batch(train_x, train_y,
                                          PreDefine.Batch_size["SVM"])
                batch_times = 0
                for data_x, data_y in batches:
                    feed = {
                        self.X: data_x,
                        self.Y: list(map(list, zip(*data_y)))
                    }

                    _, loss = self.sess.run([self.Train_op, self.Loss], feed_dict=feed)

                    batch_times += 1
                if step % 20 == 0:
                    acc = self.Predict_ACC.eval(
                        feed_dict={
                            self.X: data_x,
                            self.Y: list(map(list, zip(*data_y))),
                            self.Prediction_gird: data_x
                        }
                    )
                    if acc >= low_acc:
                        low_acc = acc
                        self.vector_x = data_x
                        self.vector_y = list(map(list, zip(*data_y)))
                    print("step %d , Loss is %f , Acc is %f" % (step, loss, acc))

            acc = 0

            # 评估准确率
            result_list = self.Predict_result.eval(
                feed_dict={
                    self.X: self.vector_x,
                    self.Y: self.vector_y,
                    self.Prediction_gird: test_x
                }
            )

            # 比较结果得到准确率
            for temp1, temp2 in zip(result_list, test_y):
                if temp1 == temp2.argmax():
                    acc += 1

            acc = acc / len(test_y)

            print("SVM model the number {0} test score is {1}".format(
                test_data['times'] + 1, acc))

            # 记录每个模型评估准确率
            new_score = acc

            if new_score >= low_score:
                low_score = new_score

                # 保存向量
                with open(PreDefine.Model_path2["SVM"] + '/vector_data', "wb") as f:
                    pk.dump(self.vector_x, f)
                    pk.dump(self.vector_y, f)

                # 保存训练的模型
                Saver = tf.train.Saver()
                Saver.save(self.sess, PreDefine.Model_path2["SVM"] + '/SVM', global_step=step)

        return low_score, new_score

        # 评估主控函数

    def SVM_test(self, data):

        # 重新训练
        # 清空原训练模型文件
        if os.path.exists(PreDefine.Model_path1['SVM']):
            for file in os.listdir(PreDefine.Model_path1['SVM']):
                os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['SVM'] + file))

        Test_data = {
            "data": data,
            "times": 0
        }
        # 区分第几折数据
        times = 0
        # 设立一个最低分,默认-100
        low_score = -100

        # 评估算法的表现
        acc_score = 0

        # 传递数据画图
        times_list = []
        new_score_list = []
        average_score_list = []

        for temp in range(PreDefine.Test_K_num):
            Test_data["times"] = times
            # new_score为每个模型的分数
            low_score, new_score = self.test_ACC(Test_data, low_score)

            times += 1
            acc_score += new_score

            times_list.append(str(times))
            new_score_list.append(new_score*100)
            average_score_list.append(acc_score / PreDefine.Test_K_num)
            yield times_list, new_score_list, average_score_list

    def SVM_prediction(self,score_data):

        result = []
        truly = []

        # 模型预测
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            Saver = tf.train.Saver()
            # 恢复模型
            Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["SVM"]))
            x_data, y_data = data_process.data_process(score_data)

            # 读取向量
            with open(PreDefine.Model_path2["SVM"] + '/vector_data', "rb") as f:
                self.vector_x = pk.load(f)
                self.vector_y = pk.load(f)

            data_len = len(x_data)

            for i in range(data_len):
                feed = {
                    self.X: self.vector_x,
                    self.Y: self.vector_y,
                    self.Prediction_gird:[x_data[i]]
                }
                print(self.sess.run(self.Predict_output, feed_dict=feed))
                result.append(self.sess.run(tf.argmax(self.Predict_output,0), feed_dict=feed)[0])
                truly.append(np.argmax(y_data[i]))

        return [result, truly]

    def SVM_train(self,model_mode,score_data):

        step_list = []
        loss_list = []
        acc_list = []

        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            # 保存训练的模型
            Saver = tf.train.Saver()

            # 初次或重新训练
            if model_mode == PreDefine.Model_mode[0]:
                # 清空原训练模型文件
                if os.path.exists(PreDefine.Model_path1['SVM']):
                    for file in os.listdir(PreDefine.Model_path1['SVM']):
                        os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['SVM'] + file))

            # 继续训练
            else:
                # 恢复模型
                Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["SVM"]))

            Batch = Batches.Load_Batch(score_data)

            # 记录最低训练分
            low_acc = 0

            for step in range(PreDefine.Train_step["SVM"]):
                batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                          PreDefine.Batch_size["SVM"])
                for data_x, data_y in batches:
                    feed = {
                        self.X: data_x,
                        self.Y: list(map(list, zip(*data_y)))
                    }

                    _, loss = self.sess.run([self.Train_op, self.Loss], feed_dict=feed)

                if step % 20 == 0:
                    acc = self.Predict_ACC.eval(
                        feed_dict={
                            self.X: data_x,
                            self.Y: list(map(list, zip(*data_y))),
                            self.Prediction_gird:data_x
                        }
                    )

                    if acc >= low_acc:
                        low_acc = acc
                        self.vector_x = data_x
                        self.vector_y = list(map(list, zip(*data_y)))

                    print("step %d , Loss is %f , Acc is %f" % (step,loss,acc))

                if step % Parameter.Model_Refresh_num == 0:
                    acc = self.Predict_ACC.eval(
                        feed_dict={
                            self.X: data_x,
                            self.Y: list(map(list, zip(*data_y))),
                            self.Prediction_gird: data_x
                        }
                    )
                    step_list.append(str(step))
                    loss_list.append(loss)
                    acc_list.append(acc*100)

                    yield step_list, loss_list, acc_list

            # 保存向量
            with open(PreDefine.Model_path2["SVM"] + '/vector_data', "wb") as f:
                pk.dump(self.vector_x, f)
                pk.dump(self.vector_y, f)

            Saver.save(self.sess, PreDefine.Model_path2["SVM"] + '/SVM', global_step=step)


class DNN:
    def __init__(self):
        self.Graph = tf.Graph()
        with self.Graph.as_default():
            self.X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["DNN"])
            self.Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["DNN"])

            self.W1 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["DNN1"], stddev=PreDefine.Normal_variable))
            self.B1 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN1"]))

            self.Layer1 = tf.nn.relu(tf.matmul(self.X, self.W1) + self.B1)

            self.W2 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["DNN2"], stddev=PreDefine.Normal_variable))
            self.B2 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN2"]))

            self.Layer2 = tf.nn.relu(tf.matmul(self.Layer1, self.W2) + self.B2)

            self.W3 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["DNN3"], stddev=PreDefine.Normal_variable))
            self.B3 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN3"]))

            self.Layer3 = tf.nn.relu(tf.matmul(self.Layer2, self.W3) + self.B3)

            self.W4 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["DNN4"], stddev=PreDefine.Normal_variable))
            self.B4 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN4"]))

            self.Layer4 = tf.nn.relu(tf.matmul(self.Layer3, self.W4) + self.B4)

            self.W5 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["DNN5"], stddev=PreDefine.Normal_variable))
            self.B5 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN5"]))

            self.Layer5 = tf.nn.relu(tf.matmul(self.Layer4, self.W5) + self.B5)

            self.W6 = tf.Variable(
                tf.truncated_normal(shape=PreDefine.W_shape["DNN6"], stddev=PreDefine.Normal_variable))
            self.B6 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["DNN6"]))

            self.Layer6 = tf.matmul(self.Layer5, self.W6) + self.B6

            # 交叉熵损失函数
            self.Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.Y, logits=self.Layer6))

            # 梯度下降优化
            self.Train_op = tf.train.AdamOptimizer(PreDefine.Learning_rate["DNN"]).minimize(self.Loss)

            # 准确率
            self.Acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(self.Y, 1), tf.argmax(self.Layer6, 1)), 'float'))

    # 评估统计
    def test_ACC(self, test_data, low_score):
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()
            Batch = Batches.Load_Batch(test_data)

            # 将数据细分出来
            train_x = Batch.Data_X['train_x_scaler_data']
            train_y = Batch.Data_Y['train_y_onehot_list']
            test_x = Batch.Data_X['test_x_scaler_data']
            test_y = Batch.Data_Y['test_y_onehot_list']

            loss = 0
            acc = 0

            for step in range(PreDefine.Train_step["DNN"]):
                batches = Batch.get_batch(train_x, train_y,
                                          PreDefine.Batch_size["DNN"])
                batch_times = 0
                for data_x, data_y in batches:
                    feed = {
                        self.X: data_x,
                        self.Y: data_y
                    }

                    _, loss = self.sess.run([self.Train_op, self.Loss], feed_dict=feed)

                    batch_times += 1

                if step % 20 == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    print("step %d , Loss is %f , Acc is %f" % (step, loss, acc))

            acc = self.Acc.eval(feed_dict={self.X: test_x, self.Y: test_y})
            print("DNN model the number {0} test score is {1}".format(
                test_data['times'] + 1, acc))

            # 记录每个模型评估准确率
            new_score = acc

            if new_score >= low_score:
                low_score = new_score
                # 保存训练的模型
                Saver = tf.train.Saver()
                Saver.save(self.sess, PreDefine.Model_path2["DNN"] + '/DNN', global_step=step)

        return low_score, new_score

        # 评估主控函数

    def DNN_test(self, data):

        # 重新训练
        # 清空原训练模型文件
        if os.path.exists(PreDefine.Model_path1['DNN']):
            for file in os.listdir(PreDefine.Model_path1['DNN']):
                os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['DNN'] + file))

        Test_data = {
            "data": data,
            "times": 0
        }
        # 区分第几折数据
        times = 0
        # 设立一个最低分,默认-100
        low_score = -100

        # 评估算法的表现
        acc_score = 0

        # 传递数据画图
        times_list = []
        new_score_list = []
        average_score_list = []

        for temp in range(PreDefine.Test_K_num):
            Test_data["times"] = times
            # new_score为每个模型的分数
            low_score, new_score = self.test_ACC(Test_data, low_score)
            times += 1
            acc_score += new_score

            times_list.append(str(times))
            new_score_list.append(new_score*100)
            average_score_list.append(acc_score / PreDefine.Test_K_num)
            yield times_list, new_score_list, average_score_list

    def DNN_prediction(self,score_data):

        result = []
        truly = []

        # 模型预测
        # 加载训练的模型
        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            Saver = tf.train.Saver()
            # 恢复模型
            Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["DNN"]))
            x_data, y_data = data_process.data_process(score_data)

            data_len = len(x_data)

            for i in range(data_len):
                feed = {
                    self.X: [x_data[i]],
                    self.Y: [y_data[i]]
                }

                print(self.sess.run(self.Layer6, feed_dict=feed))
                result.append(np.argmax(self.sess.run(self.Layer6, feed_dict=feed)))
                truly.append(np.argmax(y_data[i]))

        return [result, truly]

    def DNN_train(self,model_mode,score_data):

        step_list = []
        loss_list = []
        acc_list = []

        with tf.Session(graph=self.Graph) as self.sess:
            tf.global_variables_initializer().run()

            # 保存训练的模型
            Saver = tf.train.Saver()

            # 初次或重新训练
            if model_mode == PreDefine.Model_mode[0]:
                # 清空原训练模型文件
                if os.path.exists(PreDefine.Model_path1['DNN']):
                    for file in os.listdir(PreDefine.Model_path1['DNN']):
                        os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['DNN'] + file))

            else:
                # 恢复模型继续训练
                Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["DNN"]))

            Batch = Batches.Load_Batch(score_data)

            for step in range(PreDefine.Train_step["DNN"]):
                batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                          PreDefine.Batch_size["DNN"])
                batch_times = 0
                for data_x, data_y in batches:
                    feed = {
                        self.X: data_x,
                        self.Y: data_y
                    }

                    _, loss = self.sess.run([self.Train_op, self.Loss], feed_dict=feed)

                    batch_times += 1

                if step % 20 == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    print("step %d , Loss is %f , Acc is %f" % (step, loss, acc))

                if step % Parameter.Model_Refresh_num == 0:
                    acc = self.Acc.eval(feed_dict=feed)
                    step_list.append(str(step))
                    loss_list.append(loss)
                    acc_list.append(acc*100)

                    yield step_list, loss_list, acc_list

            print("Train acc is " + str(self.Acc.eval(feed_dict={self.X: Batch.Data_X, self.Y: Batch.Data_Y})))
            Saver.save(self.sess, PreDefine.Model_path2["DNN"] + '/DNN', global_step=step)


if __name__ == '__main__':
    # PreDefine.Model_mode[0] strat train
    # PreDefine.Model_mode[1] keep on train
    # PreDefine.Model_mode[2] prediction
    pass