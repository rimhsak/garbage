import numpy as np
import tensorflow as tf

def my_func(arg):
    arg = tf.convert_to_tensor(arg, dtype=tf.float32)
    return arg

# The following calls are equivalent.
value_1 = my_func(tf.constant([[1.0, 2.0], [3.0, 4.0]]))
value_2 = my_func([[1.0, 2.0], [3.0, 4.0]])
value_3 = my_func(np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32))

with tf.Session() as sess:
    print(sess.run(value_1))

