import time

from user.user_trainer import UserTrainer
from user.user_config import UserConfig

from dataflow.data_flow import Dataflow, AugmentedDataflow
from dataflow.parallel import *
from dataflow.batch_data import BatchData

import tensorflow as tf

from tensorpack.dataflow import *

if __name__ == '__main__':
    print("Start!!")

    config = UserConfig()
    user_trainer = UserTrainer(config, 'train')
    #dataflow = Dataflow(user_trainer)
    dataflow = Dataflow(user_trainer)
    dataflow = MultiThreadPrefetchData(dataflow, config.batch_size, 2)
    dataflow.reset()

    dataflow = BatchData(dataflow, config.batch_size)
    #dataflow = BatchPrefetchData(dataflow, 10, 1)
    #dataflow.reset()
    time.sleep(1)
    
    lcount = 0
    for i in dataflow.get_data():
        print(i)
        #print(str(lcount+1) + ": " + str(i[1].shape))
#        lcount += 1
#        if lcount == 20:
#            dataflow.stop()

    #print(next(dataflow.get_data())[1].shape)
    #print(next(dataflow.get_data())[0].shape)

    #data = next(dataflow.get_data())
    #time.sleep(1)
    #print(next(dataflow.get_data())[1])



