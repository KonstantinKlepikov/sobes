import threading
import time


def worker_with(lock, t: float):
    with lock:
        print(f'Lock with {t}')
        time.sleep(t)
    print(f'im sleep {t}')


lock = threading.Lock()
w1 = threading.Thread(target=worker_with, args=(lock, 0.5))
w2 = threading.Thread(target=worker_with, args=(lock, 0.4))

w1.start()
w2.start()
