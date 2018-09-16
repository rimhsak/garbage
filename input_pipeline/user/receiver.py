from tensorpack.dataflow import *
import numpy as np

df = RemoteDataZMQ('tcp://127.0.0.1:8888')
local_count = 0
while True:
    data = next(df.get_data())
    print(local_count, len(data))
    local_count+=1
    #print(data[2], data[3])
       
