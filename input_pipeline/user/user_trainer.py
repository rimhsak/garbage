import time
from itertools import cycle
from six.moves import configparser

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from user_config import UserConfig

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'nabu') )

from nabu.processing.processors import processor_factory

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
        print("Getting Data")
        splitline = next(self._dataflow[0]).strip().split(' ')
        name = splitline[0]
        dataline = ' '.join(splitline[1:])
        #print(dataline)
        processed = self.processor(dataline)
        #print(processed)

        text_splitline = next(self._dataflow[1]).strip().split(' ')
        text_name = text_splitline[0]
        text_dataline = ' '.join(text_splitline[1:])
        #print(text_dataline)
        text_processed = self.text_processor(text_dataline)
        #print(text_processed)

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

if __name__ == '__main__':
    userConfig = UserConfig()
    userTrainer = UserTrainer(userConfig, 'train')
    userTrainer.InitData()
    userTrainer.GetData()
#    count = 0
#    while True:
#        userTrainer.GetData()
#        if count == 10:
#            break
#        count += 1
#    print("end")
