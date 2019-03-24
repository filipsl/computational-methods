# Created by Filip Slazyk
# MOwNiT 2
# 2018/2019

import numpy as np
import math
import timeit


def check_result(a, b, x):
    tol = 1e-5
    res = a @ x
    for i in range(0, len(a)):
        if not math.isclose(abs(b[i] - res[i]), 0, abs_tol=tol):
            return False

    return True


def gauss_jordan(a, b):
    a = np.hstack([a, b.reshape(-1, 1)])
    n = len(a)
    permutation_vector = list(range(0, n))

    global_abs_max_el = max(a.max(), abs(a.min()))
    a = a / global_abs_max_el

    for i in range(0, n):
        max_el = abs(a[i][i])
        max_row = i
        max_col = i

        for j in range(i, n):  # go downward by rows
            for k in range(i, n):
                if abs(a[j][k]) > max_el:
                    max_el = abs(a[j][k])
                    max_row = j
                    max_col = k

        a[:, [i, max_col]] = a[:, [max_col, i]]  # swap columns
        permutation_vector[i], permutation_vector[max_col] = permutation_vector[max_col], permutation_vector[i]

        for j in range(i, n + 1):  # swap rows - loop is more efficient as it does not iterate through zeros
            a[[max_row, i], j] = a[[i, max_row], j]

        for k in range(i + 1, n):
            c = -a[k][i] / a[i][i]
            for j in range(i, n + 1):
                if i == j:
                    a[k][j] = 0
                else:
                    a[k][j] += c * a[i][j]

        for k in range(0, i):
            c = -a[k][i] / a[i][i]
            for j in range(i, n + 1):
                if i == j:
                    a[k][j] = 0
                else:
                    a[k][j] += c * a[i][j]

        if a[i][i] != 0:
            a[i] = a[i] / a[i][i]

    a[permutation_vector, n] = a[[list(range(0, n))], n]  # swap variables according to permutation vector

    return a[:, n]


for i in [100, 500, 750, 1000, 1250]:
    print('Matrix ', i, 'x', i)

    a = np.random.randn(i, i)
    b = np.random.random(i)

    start = timeit.default_timer()
    x = gauss_jordan(a, b)
    stop = timeit.default_timer()
    print("Valid result?: ", check_result(a, b, x))
    print('My function: ', stop - start, "s")

    start = timeit.default_timer()
    x = np.linalg.solve(a, b)
    stop = timeit.default_timer()
    print('np.linalg.solve function: ', stop - start, "s")

    start = timeit.default_timer()
    x = np.linalg.lstsq(a, b, rcond=None)[0]
    stop = timeit.default_timer()
    print('np.linalg.lstsq function: ', stop - start, "s")

    print("\n")
