import time
from threading import Thread


def do_work(s: int):
    print(f"Starting work on: {s}")
    time.sleep(1)
    print(f"Finished work on: {s}")


if __name__ == '__main__':
    for n in range(5):
        t = Thread(target=do_work, args=(n,))
        t.start()