import multiprocessing
from multiprocessing.context import Process

import time


def print_array_contents(array):
    while True:
        print(*array, sep = ", ")
        time.sleep(0.5)


if __name__ == '__main__':
    """ in this example we pass mutable as param...
    Q: why mutable is printed as -1 and not seeing the change?
    because when we create process you got separate memory
    """
    #arr = [-1] * 10
    # typecode_or_type, size_or_initializertypecode_or_type, size_or_initializer, Lock=True
    arr = multiprocessing.Array('i', [-1] * 10)
    p = Process(target=print_array_contents, args=(arr,))
    p.start()
    for j in range(10):
        time.sleep(1)
        for i in range(10):
            arr[i] = j
