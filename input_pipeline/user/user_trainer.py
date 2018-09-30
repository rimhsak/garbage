import time
from itertools import cycle
from six.moves import configparser

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from user_config import UserConfig

import os
import sys
import threading

sys.path.insert(0, os.path.join(os.getcwd(), 'nabu') )

from nabu.processing.processors import processor_factory
import numpy as np

from tensorpack.dataflow import *
class UserTrainer:

    def __init__(self, config, mode=None):
        self._config = config
        self._mode = mode
        self._dataflow = None
        pass

    def InitData(self):
        """
        initialize dataflow as the mode

        :return: initialized dataflow
        """

        config = self._config
       
        # speech data
        parsed_cfg = configparser.ConfigParser()
        parsed_cfg.read(os.path.join(config.train_data_expdir, 'database.conf'))

        name = parsed_cfg.sections()[0]

        conf = dict(parsed_cfg.items(name))

        proc_cfg = configparser.ConfigParser()
        proc_cfg.read(os.path.join(config.train_data_expdir, 'processor.cfg'))

        self.processor = processor_factory.factory(proc_cfg.get('processor', 'processor'))(proc_cfg)
        datafile = conf['datafiles'].split(' ')[0]
        
        #self._dataflow = cycle(open(datafile).readlines())

        # text data
        text_parsed_cfg = configparser.ConfigParser()
        text_parsed_cfg.read(os.path.join(config.train_text_data_expdir, 'database.conf'))

        text_data_name = text_parsed_cfg.sections()[0]

        text_conf = dict(text_parsed_cfg.items(text_data_name))

        text_proc_cfg = configparser.ConfigParser()
        text_proc_cfg.read(os.path.join(config.train_text_data_expdir, 'processor.cfg'))
        
        self.text_processor = processor_factory.factory(text_proc_cfg.get('processor', 'processor'))(text_proc_cfg)
        text_datafile = text_conf['datafiles'].split(' ')[0]
        
        self._dataflow = ( cycle(open(datafile).readlines()), cycle(open(text_datafile).readlines()) )
        self._alphabet = dict(text_proc_cfg.items('processor'))['alphabet'].split(' ')
        print(self._alphabet)
        
        self._lookup = dict()
        for i in range(len(self._alphabet)):
            self._lookup[self._alphabet[i]] = i

        print(self._lookup)
        #print(len(open(datafile).readlines()))
        return self._dataflow

    def GetData(self):
        """
        get a data from the dataflow
        a data is like (data, label)
        :return: data maybe numpy format
        """
        #count = 0
        #while count != 4 :
        #    print(next(self._dataflow))
        #    count += 1
        #for i in init_dataflow:
        #    print(i)
        #print("Getting Data")
        splitline = next(self._dataflow[0]).strip().split(' ')
        name = splitline[0]
        dataline = ' '.join(splitline[1:])
        #print(dataline)
        processed = np.asarray(self.processor(dataline))
        #print(processed)
        #print(len(processed))

        text_splitline = next(self._dataflow[1]).strip().split(' ')
        text_name = text_splitline[0]
        text_dataline = ' '.join(text_splitline[1:])
        #print(text_dataline)
        text_processed = self.text_processor(text_dataline)
        #print(text_processed)
        
        encode_text_processed = list()
        for i in (text_processed.split(' ')):
            if i == '':
                continue
            encode_text_processed.append( self._lookup[i] )
        text_processed = np.asarray(encode_text_processed).astype('int')

        #
        
        #return (self._dataflow[0], self._dataflow[1])
        return (processed, text_processed)

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

class MyDataFlow(DataFlow):
    def __init__(self, userTrainer):
        super(MyDataFlow, self).__init__()
        self.user_trainer = userTrainer
        self.user_trainer.InitData()
        self.is_stop = True

    def size(self):
        return 2162

    def get_data(self):
        #while self.is_stop:
        for i in range(self.size()):
            yield self.user_trainer.GetData()

    def reset_state(self):
        self.is_stop = False

#class MyThreadDataFlow(DataFlow, thread.Threading):
#    def __init__(self, ds, batch
    
class MyBatchData(ProxyDataFlow):

    def __init__(self, ds, batch):
        super(MyBatchData, self).__init__(ds)
        self.batch = batch
        self.ds = ds

    def size(self):
        return self.ds.size() // self.batch

    def get_data(self):
        itr = self.ds.get_data()
        while True:
            feats = []
            labs = []
            for _ in range(self.batch):
                feat, lab = next(itr)
                feats.append(feat)
                labs.append(lab)

            batch_feat, feat_len = self.batch_feat(feats)
            batch_lab, lab_len = self.batch_lab(labs)
            yield [batch_feat, feat_len, batch_lab, lab_len]

    def batch_feat(self, feats):
        max_len = max([d.shape[0] for d in feats])
        batch_size = len(feats)
        batched = np.zeros((batch_size, max_len, feats[0].shape[1]))
        batched_len = np.zeros(batch_size).astype('int')
        for idx, feat in enumerate(feats):
            batched[idx, :feat.shape[0], :] = feat
            batched_len[idx] = feat.shape[0]
        return batched, batched_len

    def batch_lab(self, labs):
        max_len = max([d.shape[0] for d in labs])
        batch_size = len(labs)
        batched = np.zeros((batch_size, max_len)).astype('int')
        batched_len = np.zeros(batch_size).astype('int')
        for idx, lab in enumerate(labs):
            batched[idx, :lab.shape[0]] = lab
            batched_len[idx] = lab.shape[0]
        return batched, batched_len

if __name__ == '__main__':
    userConfig = UserConfig()
    userTrainer = UserTrainer(userConfig, 'train')
    
    ds = MyDataFlow(userTrainer)
    #ds = PrefetchData(ds, 128, 2)
    ds = MyBatchData(ds, 32)
    #ds = PrefetchData(ds, 8, 1)

    send_dataflow_zmq(ds, 'tcp://127.0.0.1:8888')
    #print(next(ds.get_data()))
     
    import tensorflow as tf

    with tf.Session() as sess:
        count = 0
        while True:
            print("*"*50 + " " + str(count))
            data = next(ds.get_data())
            
            inputs = tf.convert_to_tensor(data[0], dtype=np.float32)
            inputs_length= tf.convert_to_tensor(data[1], dtype=np.int32)
            targets= tf.convert_to_tensor(data[2], dtype=np.int32)
            targets_length= tf.convert_to_tensor(data[3], dtype=np.int32)
            print(sess.run([inputs, inputs_length, targets, targets_length]))
            print(inputs)
    
            if count == 11:
                break
            count += 1
    #    print("end")
