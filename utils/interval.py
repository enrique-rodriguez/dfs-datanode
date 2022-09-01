import time
import uuid
import threading


intervals = dict()
lock = threading.Lock()


def worker(func, args, interval, int_id):
    running = True
    while running:
        func(*args)
        time.sleep(interval)
        lock.acquire()
        running = intervals.get(int_id, False)
        lock.release()


def set_interval(func, args, interval):
    int_id = uuid.uuid4().hex
    thread = threading.Thread(target=worker, args=(func, args, interval, int_id))
    lock.acquire()
    intervals[int_id] = (True, thread)
    lock.release()
    thread.start()
    return int_id


def clear_interval(int_id):
    lock.acquire()
    _, thread = intervals[int_id]
    del intervals[int_id]
    lock.release()
    thread.join()
