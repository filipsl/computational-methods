# Created by Filip Slazyk
# MOwNiT 2
# 2018/2019

import scipy.linalg
import numpy as np
import timeit


def lu_decomposition(b):
    a = np.copy(b)
    n = len(a)
    L = np.zeros((n, n), float)
    np.fill_diagonal(L, 1)
    for i in range(0, n):
        for j in range(i + 1, n):
            c = a[j][i] / a[i][i]
            for k in range(i, n):
                a[j][k] -= a[i][k] * c
            L[j][i] = c

    U = np.zeros((n, n))

    for i in range(0, n):
        for j in range(i, n):
            U[i][j] = a[i][j]

    return L, U


def lu_decomposition_with_pivoting(b):
    a = np.copy(b)
    n = len(a)
    L = np.zeros((n, n), float)
    P = np.zeros((n, n), float)
    np.fill_diagonal(P, 1)
    U = a

    s = np.zeros(n)
    permutation_vector = list(range(0, n))

    for i in range(0, n):
        s[i] = max(abs(U[i][i:n]))

    for i in range(0, n):
        max_row = i
        pivot = 0

        for j in range(i, n):
            if pivot < abs(U[j][i] / s[permutation_vector[j]]):
                max_row = j
                pivot = abs(U[j][i] / s[permutation_vector[j]])


        U[[i, max_row], :] = U[[max_row, i], :]
        P[[i, max_row], :] = P[[max_row, i], :]
        L[[i, max_row], :] = L[[max_row, i], :]

        permutation_vector[i], permutation_vector[max_row] \
            = permutation_vector[max_row], permutation_vector[i]

        L[i:n, i] = U[i:n, i] / U[i][i]

        l_temp = L[(i + 1):n, i]

        U[(i + 1):n, i:n] = U[(i + 1):n, i:n] - U[i, i:n] * l_temp[:, np.newaxis]

    for i in range(0, n):
        for j in range(i + 1, n):
            U[j][i] = 0
            L[i][j] = 0

    np.fill_diagonal(L, 1)
    return P, L, U


for i in [100, 250, 500, 750, 1000]:
    print('Matrix ', i, 'x', i)

    a = np.random.randn(i, i)

    start = timeit.default_timer()
    P, L, U = lu_decomposition_with_pivoting(a)
    stop = timeit.default_timer()
    print("Valid result?: ", np.allclose(P @ a, L @ U, atol=1e-10))
    print('My function: ', stop - start, "s")

    start = timeit.default_timer()
    P, L, U = scipy.linalg.lu(a)
    stop = timeit.default_timer()
    print('scipy.linalg.lu function: ', stop - start, "s")

    print("\n")
