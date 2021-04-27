from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, as_completed
import time


def sleep_task(sec):
    print("sleeping {} second begin!".format(sec))
    time.sleep(sec)
    print("sleeping {} second end!".format(sec))


executor = ThreadPoolExecutor(max_workers=2)
task1 = executor.submit(sleep_task, 2)
task2 = executor.submit(sleep_task, 2)
task3 = executor.submit(sleep_task, 2)

all_task = [task1, task2, task3]

for t in as_completed(all_task):
    print(t.result())

if __name__ == '__main__':
    pass

