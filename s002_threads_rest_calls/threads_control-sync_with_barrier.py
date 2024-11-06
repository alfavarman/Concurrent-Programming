import time
from random import randint
from threading import Thread, Barrier
from typing import List

matrix_size = 10



def generate_random_matrix(matrix_size: int, range_n: int) -> List[List[int]]:
    return [[randint(-range_n, range_n) for _ in range(matrix_size)] for _ in range(matrix_size)]


def randomize_matrix(matrix, range_n=5):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = randint(-range_n, range_n)


def multiply_matrixes(m1, m2, r, size, end_msg):
    for row in range(size):
        for col in range(size):
            for i in range(size):
                r[row][col] += m1[row][i] * m2[i][col]
    print(f"finished: {end_msg}")


def sync_calc():
    for i in range(10):
        matrix_a = generate_random_matrix(matrix_size, 5)
        matrix_b = generate_random_matrix(matrix_size, 5)
        result = [[0] * matrix_size for _ in range(matrix_size)]
        msg = f"S:{i}"
        multiply_matrixes(matrix_a, matrix_b, result, matrix_size, msg)

def thread_calc():
    threads = []
    for i in range(10):
        matrix_a = generate_random_matrix(matrix_size, 5)
        matrix_b = generate_random_matrix(matrix_size, 5)
        result = [[0] * matrix_size for _ in range(matrix_size)]
        msg = f"T:{i}"
        t = Thread(target=multiply_matrixes, args=(matrix_a, matrix_b, result, matrix_size, msg))
        t.start()
        threads.append(t)
    [t.join() for t in threads]

def threads_with_b():
    """
    Barrier is released once all threads comes to .wait().
    Init barrier with all child threads.wait().
    As only last thread will get to wait() barrier will be released.

    Second Barrier - complete will get Main thread.wait(). and wait for others to get there.
    """
    work_start = Barrier(matrix_size + 1)
    work_complete = Barrier(matrix_size + 1)

    matrix_a = generate_random_matrix(matrix_size, 5)
    matrix_b = generate_random_matrix(matrix_size, 5)
    result = [[0] * matrix_size for _ in range(matrix_size)]

    def multiply_row(row):
        while True:
            work_start.wait()
            for col in range(matrix_size):
                for i in range(matrix_size):
                    result[row][col] += matrix_a[row][i] * matrix_b[i][col]
            work_complete.wait()

    for row in range(matrix_size):
        t = Thread(target=multiply_row, args=(row,))
        t.start()

    for i in range(10):
        randomize_matrix(matrix_a)
        randomize_matrix(matrix_b)
        result = [[0] * matrix_size for _ in range(matrix_size)]
        work_start.wait()
        work_complete.wait()
        print(f"finished: TB:{i}")

start0 = time.time()
sync_calc()
end0 = time.time()

start1 = time.time()
thread_calc()
end1 = time.time()

start2 = time.time()
threads_with_b()
end2 = time.time()


print("Time Sync: ", end0 - start0)
print("Time Threads: ", end1 - start1)
print("Time Threads with barrier: ", end2 - start2)
