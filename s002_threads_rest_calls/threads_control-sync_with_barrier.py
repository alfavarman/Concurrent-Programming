import time
from random import randint
from threading import Thread
from typing import List


def generate_random_matrix(matrix_size: int, range_n: int) -> List[List[int]]:
    return [[randint(-range_n, range_n) for _ in range(matrix_size)] for _ in range(matrix_size)]

def multiply_matrixes(m1, m2, r, size, end_msg):
    for row in range(size):
        for col in range(size):
            for i in range(size):
                r[row][col] += m1[row][i] * m2[i][col]
    print(f"finished: {end_msg}")

matrix_size = 100
matrix_a = generate_random_matrix(matrix_size, 5)
matrix_b = generate_random_matrix(matrix_size, 5)
result = generate_random_matrix(matrix_size, 0)

start0 = time.time()
for i in range(10):
    result = [[0] * matrix_size for _ in range(matrix_size)]
    msg = f"S:{i}"
    multiply_matrixes(matrix_a, matrix_b, result, matrix_size, msg)
end0 = time.time()


threads = []
start1 = time.time()
for i in range(10):
    result = [[0] * matrix_size for _ in range(matrix_size)]
    msg = f"T:{i}"
    t = Thread(target=multiply_matrixes, args=(matrix_a, matrix_b, result, matrix_size, msg))
    t.start()
    threads.append(t)
[t.join() for t in threads]
end1 = time.time()


print("Time Sync: ", end0 - start0)
print("Time Threads: ", end1 - start1)
