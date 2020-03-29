import tensorflow as tf
import path_define as PreDefine
import Data_process as data_process
import Batches
import os
import numpy as np


class logistics_regression:
    def __init__(self):
        self.X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["logistics_regression"])
        self.Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["logistics_regression"])
        self.W = tf.Variable(
            tf.truncated_normal(shape=PreDefine.W_shape["logistics_regression"], stddev=PreDefine.Normal_variable))
        self.B = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["logistics_regression"]))

        # with tf.name_scope("Result"):
        self.Result = tf.nn.softmax(tf.matmul(self.X, self.W) + self.B)
        # with tf.name_scope("Loss"):
        self.Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.Result, labels=self.Y))
        # with tf.name_scope("Train_op"):
        self.Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["logistics_regression"]).minimize(self.Loss)
        # with tf.name_scope("Accuracy"):
        self.Acc = tf.reduce_mean(tf.cast(tf.equal(self.Result, self.Y), tf.float32))
        self.sess = tf.InteractiveSession()
        # 用来显示标量信息
        # tf.summary.scalar("loss", self.Loss)
        # tf.summary.scalar("accuracy", self.Acc)

    # def logistics_regression_test():
    #     pass

    def logistics_regression_prediction(self,score_data):
        # 模型预测
        # 加载训练的模型

        tf.global_variables_initializer().run()

        Saver = tf.train.Saver()
        # 恢复模型
        Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["logistics_regression"]))
        x_data, y_data = data_process.data_process(score_data)

        data_len = len(x_data)

        for i in range(data_len):
            feed = {
                self.X: [x_data[i]],
                self.Y: [y_data[i]]
            }

            print("the System prediction is {0} , the truely result is {1}".format(
                np.argmax(self.sess.run(self.Result, feed_dict=feed)), np.argmax(y_data[i])))
            # 此处待添加可视化展示预测结果

    def logistics_regression_train(self,model_mode,score_data):

        tf.global_variables_initializer().run()

        # 保存训练的模型
        Saver = tf.train.Saver()

        # 将所有summary全部保存到磁盘，以便tensorboard显示
        # self.Merged_summary_op = tf.summary.merge_all()

        # 指定一个文件用来保存图。tf.get_default_graph()可以获取当前默认的计算图
        # summary_writer = tf.summary.FileWriter(PreDefine.tensorBoard_path['logistics_regression'],
        #                                        graph=tf.get_default_graph())

        # 初次或重新训练
        if model_mode == PreDefine.Model_mode[0]:
            # 清空原训练模型文件
            if os.path.exists(PreDefine.Model_path1['logistics_regression']):
                for file in os.listdir(PreDefine.Model_path1['logistics_regression']):
                    os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['logistics_regression'] + file))

        else:
            # 恢复模型继续训练
            Saver.restore(self.sess, tf.train.latest_checkpoint(PreDefine.Model_path2["logistics_regression"]))

        Batch = Batches.Load_Batch(score_data)

        for step in range(PreDefine.Train_step["logistics_regression"]):
            batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                      PreDefine.Batch_size["logistics_regression"])
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
                #     summary_writer.add_summary(merged_summary_op, step*PreDefine.Batch_num1['logistics_regression']+batch_times)
                # else:
                #     summary_writer.add_summary(merged_summary_op, step*PreDefine.Batch_num2['logistics_regression']+batch_times)

                batch_times+=1

            if step % 20 == 0:
                print("step %d , Loss is %f , Acc is %f" % (step,loss,self.Acc.eval(feed_dict=feed)))

        Saver.save(self.sess,PreDefine.Model_path2["logistics_regression"]+'/logistics_regression',global_step=step)

# def SVM_test():
#     pass


def SVM_prediction():
    pass


def SVM_train(model_mode):
    X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["SVM"])
    Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["SVM"])
    W = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["SVM"], stddev=PreDefine.Normal_variable))
    B = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["SVM"]))

    # 径向基函数（RBF）

    # 线性模型
    linear_model = tf.subtract(tf.matmul(X, W),B)

    # L2范数
    L2_norm = tf.reduce_sum(tf.square(W))

    # hinge损失函数 max(0, 1-pred*actual)
    hinge = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(linear_model, Y))))
    # Loss = hinge + alpha * L2_norm
    alpha = tf.constant([0.01])
    Loss = tf.add(hinge,tf.multiply(alpha,L2_norm))
    Acc = tf.reduce_mean(tf.cast(tf.equal(linear_model, Y), tf.float32))

    # 梯度下降优化
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["SVM"]).minimize(Loss)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # 模型预测
    if model_mode == PreDefine.Model_mode[2]:
        # 加载训练的模型
        Saver = tf.train.Saver()
        # 恢复模型
        Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["SVM"]))

        Batch = Batches.Load_Batch()
        data_len = len(Batch.Data_X)
        for i in range(5):
            feed = {
                X: Batch.Data_X[data_len - i - 1:],
                Y: Batch.Data_Y[data_len - i - 1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(
                np.argmax(sess.run(linear_model, feed_dict=feed)), np.argmax(Batch.Data_Y[data_len - i - 1:])))

    else:
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
            Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["SVM"]))

        Batch = Batches.Load_Batch()

        for step in range(PreDefine.Train_step["SVM"]):
            batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                      PreDefine.Batch_size["SVM"],model_mode)
            for data_x, data_y in batches:
                feed = {
                    X: data_x,
                    Y: data_y
                }

                _, loss = sess.run([Train_op, Loss], feed_dict=feed)

            if step % 20 == 0:
                print("step %d , Loss is %f , Acc is %f" % (step, loss, Acc.eval(feed_dict=feed)))

        Saver.save(sess, PreDefine.Model_path2["SVM"] + '/SVM', global_step=step)

# def BP_test():
#     pass


def BP_prediction():
    pass


def BP_train(model_mode):
    X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["BP"])
    Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["BP"])
    W1 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["BP1"], stddev=PreDefine.Normal_variable))
    B1 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["BP1"]))
    W2 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["BP2"], stddev=PreDefine.Normal_variable))
    B2 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["BP2"]))

    # 单隐藏层神经网络
    Layer_output = tf.matmul(tf.nn.relu(tf.matmul(X, W1) + B1),W2) + B2

    # 交叉熵损失函数
    Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=Layer_output))

    # 梯度下降优化
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["SVM"]).minimize(Loss)

    # 准确率
    Acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(Y, 1), tf.argmax(Layer_output, 1)), 'float'))

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # 模型预测
    if model_mode == PreDefine.Model_mode[2]:
        # 加载训练的模型
        Saver = tf.train.Saver()
        # 恢复模型
        Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["BP"]))

        Batch = Batches.Load_Batch()
        data_len = len(Batch.Data_X)
        for i in range(5):
            feed = {
                X: Batch.Data_X[data_len - i - 1:],
                Y: Batch.Data_Y[data_len - i - 1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(
                np.argmax(sess.run(Layer_output, feed_dict=feed)),
                np.argmax(Batch.Data_Y[data_len - i - 1:])))

    else:
        # 保存训练的模型
        Saver = tf.train.Saver()

        # 初次或重新训练
        if model_mode == PreDefine.Model_mode[0]:
            # 清空原训练模型文件
            if os.path.exists(PreDefine.Model_path1['BP']):
                for file in os.listdir(PreDefine.Model_path1['BP']):
                    os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['BP'] + file))

        # 继续训练
        else:
            # 恢复模型
            Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["BP"]))

        Batch = Batches.Load_Batch()

        for step in range(PreDefine.Train_step["BP"]):
            batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                      PreDefine.Batch_size["BP"],model_mode)
            for data_x, data_y in batches:
                feed = {
                    X: data_x,
                    Y: data_y
                }

                _,loss = sess.run([Train_op, Loss], feed_dict=feed)
            if step % 20 == 0:
                print("step %d , Loss is %f , Acc is %f" % (step, loss, Acc.eval(feed_dict=feed)))

        Saver.save(sess, PreDefine.Model_path2["BP"] + '/BP', global_step=step)


def CNN_train(model_mode):
    X = tf.placeholder(dtype=tf.float32, shape=PreDefine.X_shape["BP"])
    Y = tf.placeholder(dtype=tf.float32, shape=PreDefine.Y_shape["BP"])
    W1 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["BP1"], stddev=PreDefine.Normal_variable))
    B1 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["BP1"]))
    W2 = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["BP2"], stddev=PreDefine.Normal_variable))
    B2 = tf.Variable(tf.constant(value=PreDefine.B_varibale, shape=PreDefine.B_shape["BP2"]))

    # 单隐藏层神经网络
    Layer_output = tf.matmul(tf.nn.relu(tf.matmul(X, W1) + B1),W2) + B2

    # 交叉熵损失函数
    Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=Layer_output))

    # 梯度下降优化
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["SVM"]).minimize(Loss)

    # 准确率
    Acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(Y, 1), tf.argmax(Layer_output, 1)), 'float'))

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # 模型预测
    if model_mode == PreDefine.Model_mode[2]:
        # 加载训练的模型
        Saver = tf.train.Saver()
        # 恢复模型
        Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["BP"]))

        Batch = Batches.Load_Batch()
        data_len = len(Batch.Data_X)
        for i in range(5):
            feed = {
                X: Batch.Data_X[data_len - i - 1:],
                Y: Batch.Data_Y[data_len - i - 1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(
                np.argmax(sess.run(Layer_output, feed_dict=feed)),
                np.argmax(Batch.Data_Y[data_len - i - 1:])))

    else:
        # 保存训练的模型
        Saver = tf.train.Saver()

        # 初次或重新训练
        if model_mode == PreDefine.Model_mode[0]:
            # 清空原训练模型文件
            if os.path.exists(PreDefine.Model_path1['BP']):
                for file in os.listdir(PreDefine.Model_path1['BP']):
                    os.remove(os.path.join(os.getcwd(), PreDefine.Model_path1['BP'] + file))

        # 继续训练
        else:
            # 恢复模型
            Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["BP"]))

        Batch = Batches.Load_Batch()

        for step in range(PreDefine.Train_step["BP"]):
            batches = Batch.get_batch(Batch.Data_X, Batch.Data_Y,
                                      PreDefine.Batch_size["BP"],model_mode)
            for data_x, data_y in batches:
                feed = {
                    X: data_x,
                    Y: data_y
                }

                _,loss = sess.run([Train_op, Loss], feed_dict=feed)
            if step % 20 == 0:
                print("step %d , Loss is %f , Acc is %f" % (step, loss, Acc.eval(feed_dict=feed)))

        Saver.save(sess, PreDefine.Model_path2["BP"] + '/BP', global_step=step)


if __name__ == '__main__':
    # PreDefine.Model_mode[0] strat train
    # PreDefine.Model_mode[1] keep on train
    # PreDefine.Model_mode[2] prediction
    # logistics_regression_train(PreDefine.Model_mode[2])
    # SVM_train(PreDefine.Model_mode[2])
    # BP_train(PreDefine.Model_mode[2])
    pass