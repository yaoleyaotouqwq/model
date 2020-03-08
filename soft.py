import tensorflow as tf

a = [[1,2],[3,4]]
b = tf.reduce_sum(tf.square(a),1)

sess = tf.Session()
print(sess.run(tf.reshape(b,[-1,1])))