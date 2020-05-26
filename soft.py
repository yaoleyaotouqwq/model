

import tensorflow as tf

# self.Gamma = tf.constant(PreDefine.RBF["Gamma"][self.table_name])
# self.Dist = tf.reshape(tf.reduce_sum(tf.square(self.X),1),[-1,1])
# self.Norm = tf.add(
#     tf.subtract(
#         self.Dist,
#         tf.multiply(2.,tf.matmul(self.X,tf.transpose(self.X)))
#     ),
#     tf.transpose(self.Dist)
# )
# self.Kernel = tf.exp(tf.multiply(self.Gamma,tf.abs(self.Norm)))

x = [[1,2,3],[4,5,6]]

X = tf.placeholder(tf.float32,[None,3])
gama = tf.constant(-10.0)

dist = tf.reshape(tf.reduce_sum(tf.square(X),1),[-1,1])

Norm = tf.add(
    tf.subtract(
        dist,
        tf.multiply(2.,tf.matmul(X,tf.transpose(X)))
    ),
    tf.transpose(dist)
)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(dist,feed_dict={X:x}))
    print(sess.run(tf.transpose(dist),feed_dict={X:x}))
    print(sess.run(Norm,feed_dict={X:x}))