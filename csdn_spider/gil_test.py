from threading import Thread
from threading import Lock
from queue import Queue

total = 0
total_lock = Lock
NUM_TIMES = 1000000


def add():
    global total
    total_lock.acquire()
    for i in range(NUM_TIMES):
        total += 1
    total_lock.release()


def sub():
    global total
    total_lock.acquire()
    for i in range(NUM_TIMES):
        total -= 1
    total_lock.release()


if __name__ == '__main__':
    addt = Thread(target=add)
    subt = Thread(target=sub)
    addt.start()
    subt.start()
    addt.join()
    subt.join()
    print(total)
