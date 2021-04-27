import time


def log(func):
    def wrapper(*args, **kwargs):
        st = time.time()
        func(*args, **kwargs)
        du = time.time() - st
        print("Spend {}h {}m {}s".format(du/3600, du/60, du))
    return wrapper
