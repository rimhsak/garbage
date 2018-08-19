import sys
import multiprocessing as mp
#from multiprocessing import Queue
import Queue
import threading
import os

from .data_flow import Dataflow
from .data_thread import *

__all__ = ['MultiThreadPrefetchData', 'BatchPrefetchData']

class MultiThreadPrefetchData(Dataflow):
    """
    create multi thread dataflow and run transformation of data in one thread
    the transformed data will be gathered in a queue
    """

    class _Worker(StoppableThread):
        def __init__(self, dataflow, queue):
            super(MultiThreadPrefetchData._Worker, self).__init__()
            self.dataflow = dataflow
            assert isinstance(self.dataflow, Dataflow), self.dataflow
            self.queue = queue
            self.daemon = True

        def run(self):
            try:
                while True:
                    if self.is_stop():
                        break
                    data= self.dataflow.get_data()
                    #print('inside _Worker')
                    #print(data[0])
                    self.queue_put_stoppable(self.queue, data)
            except Exception as e:
                #print(e)
                if self.is_stop():
                    pass
                else:
                    raise
            finally:
                print("stop()")
                self.stop()

    def __init__(self, dataflow, queue_size=100, num_thread=1):
        """

        :param dataflow:
        :param queue_size: queue size
        :param num_thread: number of threads
        """
        super(Dataflow, self).__init__()
        assert queue_size > 0 and num_thread > 0
        self.num_thread = num_thread
        self.queue = Queue.Queue(maxsize=queue_size)
        self.dataflow = dataflow
        self.dataflow.reset()
        #print("num_thread: %d" % num_thread)
        #print("queue_size: %d"% queue_size)
        self.threads = [
            MultiThreadPrefetchData._Worker(self.dataflow, self.queue)
            for _ in range(num_thread)]

    def reset(self):
        for th in self.threads:
            th.start()

    def get_data(self):
        #print("In MultiThreadPrefetch, get_data()")
        while True:
            data = self.queue.get()
            yield data
            print("in multi thread prefetch, %s"%data[1])

    def __del__(self):
        for th in self.threads:
            if th.is_alive():
                th.stop()
                th.join()


class BatchPrefetchData(Dataflow):
    """
    create multi thread dataflow and run transformation of data in one thread
    the transformed data will be gathered in a queue
    """

    class _Worker(StoppableThread):
        def __init__(self, dataflow, queue):
            self._lock = threading.Lock()
            super(BatchPrefetchData._Worker, self).__init__(lock=self._lock)
            self.dataflow = dataflow
            assert isinstance(self.dataflow, Dataflow), self.dataflow
            self.queue = queue
            self.daemon = True

        def run(self):
            try:
                while True:
                    if self.is_stop():
                        break
                    data = self.dataflow.get_data()
                    self.queue_put_stoppable(self.queue, data)
            except Exception as e:
                if self.is_stop():
                    pass
                else:
                    raise
            finally:
                print("batch stop()")
                self.stop()

    def __init__(self, dataflow, queue_size=100, num_thread=1):
        """

        :param dataflow:
        :param queue_size: queue size
        :param num_thread: number of threads
        """
        super(Dataflow, self).__init__()
        assert queue_size > 0 and num_thread > 0
        self.num_thread = num_thread
        self.queue = Queue.Queue(maxsize=queue_size)
        self.dataflow = dataflow
        print("num_thread: %d" % num_thread)
        print("queue_size: %d"% queue_size)
        self.threads = [
            BatchPrefetchData._Worker(self.dataflow, self.queue)
            for _ in range(num_thread)]

    def reset(self):
        for th in self.threads:
            th.start()

    def get_data(self):
        return self.queue.get()

    def stop(self):
        self.dataflow.stop()

    def __del__(self):
        for th in self.threads:
            if th.is_alive():
                th.stop()
                th.join()
