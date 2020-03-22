import tensorflow as tf
import path_define as PreDefine
import Data_process as data_process
import Batches
import os
import numpy as np

# def linear_regression_test():
#     pass


def linear_regression_prediction():
    pass


def linear_regression_train(model_mode):
    X = tf.placeholder(dtype=tf.float32,shape=PreDefine.X_shape["linear_regression"])
    Y = tf.placeholder(dtype=tf.float32,shape=PreDefine.Y_shape["linear_regression"])
    W = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["linear_regression"],stddev=PreDefine.Normal_variable))
    B = tf.Variable(tf.constant(value=PreDefine.B_varibale,shape=PreDefine.B_shape["linear_regression"]))

    Result = tf.nn.softmax(tf.matmul(X,W) + B)

    Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Result,labels=Y))
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["linear_regression"]).minimize(Loss)
    Acc = tf.reduce_mean(tf.cast(tf.equal(Result, Y), tf.float32))

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # 模型预测
    if model_mode == PreDefine.Model_mode[2]:
        # 加载训练的模型
        Saver = tf.train.Saver()
        # 恢复模型
        Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["linear_regression"]))

        Batch = Batches.Load_Batch()
        data_len = len(Batch.linear_regression_X)
        for i in range(5):
            feed = {
                X:Batch.linear_regression_X[data_len-i-1:],
                Y:Batch.linear_regression_Y[data_len-i-1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(np.argmax(sess.run(Result,feed_dict=feed)),np.argmax(Batch.linear_regression_Y[data_len-i-1:])))

    else:
        # 保存训练的模型
        Saver = tf.train.Saver()

        # 初次或重新训练
        if model_mode == PreDefine.Model_mode[0]:
            # 清空原训练模型文件
            if os.path.exists(PreDefine.Model_path1['linear_regression']):
                for file in os.listdir(PreDefine.Model_path1['linear_regression']):
                    os.remove(os.path.join(os.getcwd(),PreDefine.Model_path1['linear_regression']+file))

        # 继续训练
        else:
            # 恢复模型
            Saver.restore(sess, tf.train.latest_checkpoint(PreDefine.Model_path2["linear_regression"]))

        Batch = Batches.Load_Batch()

        for step in range(PreDefine.Train_step["linear_regression"]):
            batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
                                      PreDefine.Batch_size["linear_regression"],model_mode)
            for data_x,data_y in batches:
                feed = {
                    X: data_x,
                    Y: data_y
                }

                _, loss = sess.run([Train_op, Loss], feed_dict=feed)

            if step % 20 == 0:
                print("step %d , Loss is %f , Acc is %f" % (step,loss,Acc.eval(feed_dict=feed)))

        Saver.save(sess,PreDefine.Model_path2["linear_regression"]+'/linear_regression',global_step=step)

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
        data_len = len(Batch.linear_regression_X)
        for i in range(5):
            feed = {
                X: Batch.linear_regression_X[data_len - i - 1:],
                Y: Batch.linear_regression_Y[data_len - i - 1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(
                np.argmax(sess.run(linear_model, feed_dict=feed)), np.argmax(Batch.linear_regression_Y[data_len - i - 1:])))

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
            batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
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
        data_len = len(Batch.linear_regression_X)
        for i in range(5):
            feed = {
                X: Batch.linear_regression_X[data_len - i - 1:],
                Y: Batch.linear_regression_Y[data_len - i - 1:]
            }
            print("the system prediction is {0} , the truely result is {1}".format(
                np.argmax(sess.run(Layer_output, feed_dict=feed)),
                np.argmax(Batch.linear_regression_Y[data_len - i - 1:])))

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
            batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
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
    linear_regression_train(PreDefine.Model_mode[2])
    SVM_train(PreDefine.Model_mode[2])
    BP_train(PreDefine.Model_mode[2])
