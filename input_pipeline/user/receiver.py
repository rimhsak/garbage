from tensorpack.dataflow import *
import numpy as np
import tensorflow as tf

with tf.Session() as sess:
    df = RemoteDataZMQ('tcp://127.0.0.1:8888')
    local_count = 0

    while True:
        data = next(df.get_data())

        inputs = tf.convert_to_tensor(data[0], dtype=np.float32)
        inputs_length = tf.convert_to_tensor(data[1], dtype=np.int32)
        targets = tf.convert_to_tensor(data[2], dtype=np.int32)
        targets_length = tf.convert_to_tensor(data[3], dtype=np.int32)
        inputs, inputs_length, targets, targets_length = sess.run([inputs,
                                                                inputs_length,
                                                                targets,
                                                                targets_length])
        print(sess.run(tf.shape(inputs)))
        print(targets)
        print(local_count)
        local_count+=1
        if local_count == 10:
            break
            
       
