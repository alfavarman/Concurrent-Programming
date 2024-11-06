import multiprocessing
import time
from random import randint
from multiprocessing import Process, Barrier, Array
from typing import List

matrix_size = 200
process_pool = 6
"""
results for size=200
Time Sync:  7.522228956222534
Time Threads:  7.599188804626465
Time Threads with barrier:  8.697989463806152
"""


def randomize_mtx(matrix: List[int], n: int = 5):
    for i in range(len(matrix)):
        matrix[i] = randint(-n, n)

def multiply_row(proc, m_1, m_2, r, work_start, work_complete):
    while True:
        work_start.wait()
        for row in range(proc, matrix_size, process_pool):
            for col in range(matrix_size):
                for i in range(matrix_size):
                    r[row * matrix_size + col] += m_1[row * matrix_size + i] * m_2[i * matrix_size + col]
        work_complete.wait()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    # work_start = Barrier(process_pool + 1)
    # work_complete = Barrier(process_pool + 1)
    n = 5
    matrix_a = Array('i', [randint(-n, n)] * matrix_size*matrix_size, lock=False)
    matrix_b = Array('i', [randint(-n, n)] * matrix_size*matrix_size, lock=False)
    result = Array('i', [0] * matrix_size*matrix_size, lock=False)

    for proc in range(process_pool):
        p = Process(target=multiply_row, args=(proc, matrix_a, matrix_b, result, work_start, work_complete))
        p.start()
    start2 = time.time()
    for i in range(10):
        randomize_mtx(matrix_a)
        randomize_mtx(matrix_b)
        result = Array('i', [0] * matrix_size * matrix_size, lock=False)
        # work_start.wait()
        # work_complete.wait()
    end2 = time.time()

    print(f"Finished in {end2 - start2}")