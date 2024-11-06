import time
from multiprocessing import Process, Array
from random import randint
from typing import List

matrix_size = 200
process_pool = 6


def randomize_mtx(matrix: List[int], n: int = 5):
    for i in range(len(matrix)):
        matrix[i] = randint(-n, n)


def multiply_rows(proc, m_1, m_2, r, size, pool_size):
    """Each process multiplies its designated rows independently."""
    for row in range(proc, size, pool_size):
        for col in range(size):
            sum_val = 0
            for i in range(size):
                sum_val += m_1[row * size + i] * m_2[i * size + col]
            r[row * size + col] = sum_val


if __name__ == '__main__':
    n = 5
    matrix_a = Array('i', [randint(-n, n)] * matrix_size * matrix_size, lock=False)
    matrix_b = Array('i', [randint(-n, n)] * matrix_size * matrix_size, lock=False)
    result = Array('i', [0] * matrix_size * matrix_size, lock=False)

    start_time = time.time()

    for iteration in range(10):
        randomize_mtx(matrix_a)
        randomize_mtx(matrix_b)

        # Create and start processes
        processes = []
        for proc in range(process_pool):
            p = Process(target=multiply_rows, args=(proc, matrix_a, matrix_b, result, matrix_size, process_pool))
            processes.append(p)
            p.start()

        # Wait for all processes to complete
        for p in processes:
            p.join()

    end_time = time.time()
    print(f"Finished in {end_time - start_time}")