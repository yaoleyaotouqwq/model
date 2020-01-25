import tensorflow as tf
import path_define as PreDefine

def linear_regression_test():
    pass

def linear_regression_prediction():
    pass


def linear_regression_train():
    X = tf.placeholder(dtype=tf.float32,shape=PreDefine.X_shape["linear_regression"])
    Y = tf.placeholder(dtype=tf.int64,shape=PreDefine.Y_shape["linear_regression"])
    W = tf.Variable(tf.truncated_normal(shape=PreDefine.W_shape["linear_regression"],stddev=PreDefine.Normal_variable))
    B = tf.Variable(tf.constant(value=PreDefine.B_varibale,shape=PreDefine.B_shape["linear_regression"]))

    Result = tf.nn.softmax(tf.matmul(X,W) + B)

    Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Result,labels=Y))
    Train_op = tf.train.GradientDescentOptimizer(PreDefine.Learning_rate["linear_regression"]).minimize(Loss)
    Acc = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(Result, 1), Y), tf.float32))

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # for step in range(PreDefine.Train_step["linear_regression"]):
    #     _,loss,acc = sess.run(Train_op,Loss,Acc,feed_dict={X:Data,Y:Data})
    #
    #     if step % 10 == 0:
    #         print("step %d Loss is %f"%(step,Loss))
    #
    #     if step % 20 == 0:
    #         print("step %d Acc is %f" % (step,Acc))


if __name__ == '__main__':
    linear_regression_train()