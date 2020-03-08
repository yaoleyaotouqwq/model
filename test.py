import tensorflow as tf
import path_define as PreDefine
import Data_process as data_process
import Batches


def linear_regression_test():
    pass


def linear_regression_prediction():
    pass


def linear_regression_train(Batch):
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

    loss = 0
    acc = 0
    for step in range(PreDefine.Train_step["linear_regression"]):
        batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
                                  PreDefine.Batch_size["linear_regression"])
        for data_x,data_y in batches:
            feed = {
                X: data_x,
                Y: data_y
            }

            _,loss,acc = sess.run([Train_op,Loss,Acc],feed_dict=feed)

        if step % 10 == 0:
            print("step %d Loss is %f"%(step,loss))

        if step % 20 == 0:
            print("step %d Acc is %f" % (step,acc))


def SVM_test():
    pass


def SVM_prediction():
    pass


def SVM_train(Batch):
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

    # 梯度下降优化
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["SVM"]).minimize(Loss)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    loss = 0
    for step in range(PreDefine.Train_step["SVM"]):
        batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
                                  PreDefine.Batch_size["SVM"])
        for data_x, data_y in batches:
            feed = {
                X: data_x,
                Y: data_y
            }

            _, loss = sess.run([Train_op, Loss], feed_dict=feed)

        if step % 10 == 0:
            print("step %d Loss is %f" % (step, loss))


def BP_test():
    pass


def BP_prediction():
    pass


def BP_train(Batch):
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

    loss = 0
    acc = 0
    for step in range(PreDefine.Train_step["BP"]):
        batches = Batch.get_batch(Batch.linear_regression_X, Batch.linear_regression_Y,
                                  PreDefine.Batch_size["BP"])
        for data_x, data_y in batches:
            feed = {
                X: data_x,
                Y: data_y
            }

            _,acc, loss = sess.run([Train_op,Acc, Loss], feed_dict=feed)

        if step % 10 == 0:
            print("step %d Loss is %f" % (step, loss))

        if step % 20 == 0:
            print("step %d Acc is %f" % (step,acc))


if __name__ == '__main__':
    Batch = Batches.Load_Batch()
    # linear_regression_train(Batch)
    # SVM_train(Batch)
    BP_train(Batch)
