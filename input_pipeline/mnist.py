import math
import sys
import tempfile
import time

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('./data', one_hot=True, seed=10).train

data = mnist.next_batch(1)

#print(data)
print(data[0].shape)
#print(X.shape)
#print(Y.shape)



