import time

from user.user_trainer import UserTrainer
from user.user_config import UserConfig

from dataflow.data_flow import Dataflow, AugmentedDataflow
from dataflow.parallel import *
from dataflow.batch_data import BatchData

if __name__ == '__main__':
    print("Start!!")

    config = UserConfig()
    user_trainer = UserTrainer('train')
    #dataflow = Dataflow(user_trainer)
    dataflow = AugmentedDataflow(user_trainer)
    dataflow = MultiThreadPrefetchData(dataflow, 100, 2)
    dataflow.reset()

    #dataflow = BatchData(dataflow, config.batch_size)
    #dataflow = BatchPrefetchData(dataflow, 4, 2)
    #dataflow.reset()
    time.sleep(1)
    #print(next(dataflow.get_data())[0].shape)

    #data = next(dataflow.get_data())
    #time.sleep(1)
    #print(next(dataflow.get_data())[1])



