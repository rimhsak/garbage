import threading
import Queue
__all__ = [ 'StoppableThread' ]

class StoppableThread(threading.Thread):

    def __init__(self, event=None, lock=None):
        """

        :param event: threading.Event
        :param lock: threading.Lock
        """
        super(StoppableThread, self).__init__()
        if event is None:
            event = threading.Event()
        self._stop_event = event
        if lock is None:
            lock = threading.Lock()
        self._lock = lock

    def stop(self):
        self._stop_event.set()

    def is_stop(self):
        return self._stop_event.is_set()

    def queue_put_stoppable(self, queue, obj):
        """
        put obj to queue
        :param queue: queue
        :param obj: object, data, something to want to put to queue
        :return: none
        """
        while not self.is_stop():
            try:
                self._lock.acquire()
                queue.put(obj, timeout=3)
                self._lock.release()
                break
            except Queue.Full:
                pass

    def queue_get_stoppable(self, queue):
        """

        :param queue: queue
        :return: object, data
        """

        while not self.is_stop():
            try:
                return queue.get(timeout=3)
            except Queue.Empty:
                pass