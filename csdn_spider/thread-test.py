import time
from threading import Thread


def sleep_task(sec):
    print("sleeping {} second begin!".format(sec))
    time.sleep(sec)
    print("sleeping {} second end!".format(sec))


class SleepThread(Thread):
    def __init__(self, sec):
        super(SleepThread, self).__init__()
        self.sleep_time = sec

    def run(self):
        print("sleeping {} second begin!".format(self.sleep_time))
        time.sleep(self.sleep_time)
        print("sleeping {} second end!".format(self.sleep_time))


if __name__ == '__main__':
    st = time.time()
    t1 = Thread(target=sleep_task, args=(3,))
    # set daemon, when main thread is finish, the sub thread will finish
    t1.setDaemon(True)
    t2 = Thread(target=sleep_task, args=(2,))
    t2.setDaemon(True)

    t1.start()
    t2.start()
    # use join to wait the sub thread finish
    t1.join()
    t2.join()
    du = time.time() - st
    print("finished in {}s".format(du))
