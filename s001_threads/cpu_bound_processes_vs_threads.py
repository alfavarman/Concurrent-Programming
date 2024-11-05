import multiprocessing

from multiprocessing import Process


def do_work(n: int):
    print(f"Starting work on: {n}")
    i = 0
    for _ in range(20000000):
        i += 1
    print(f"Finished work: {n + i}")


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    for n in range(5):
        p = Process(target=do_work, args=(n, ))
        p.start()
