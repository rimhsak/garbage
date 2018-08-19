import time

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

class UserTrainer:

    def __init__(self, mode):
        self._mode = mode
        self._dataflow = None
        pass

    def InitData(self):
        """
        initialize dataflow as the mode

        :return: initialized dataflow
        """

        if self._mode == 'train':
            self._dataflow = input_data.read_data_sets('./data', one_hot=True, seed=10).train
        elif self._mode == 'valid':
            self._dataflow = input_data.read_data_sets('./data', one_hot=True, seed=10).validation
        elif self._mode == 'test':
            self._dataflow = input_data.read_data_sets('./data', one_hot=True, seed=10).test

        return self._dataflow

    def GetData(self):
        """
        get a data from the dataflow
        a data is like (data, label)
        :return: data maybe numpy format
        """
        data, label = self._dataflow.next_batch(1)
        return (data[0], label[0])

    def TransformData(self, data):
        """
        :param data: pure data before transforming
        :return: transformed data
        """

        time.sleep(0.001) #dummy example
        #print('TRANSFORMING')
        transformed_data = data

        return transformed_data

    def GetMode(self):
        return self._mode