import numpy as np


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
            if pivot < abs(U[j][i]/s[permutation_vector[j]]):
                max_row = j
                pivot = abs(U[j][i]/s[permutation_vector[j]])

        for j in range(i + 1, n):
            if abs(U[j][i]) == pivot:
                max_row = j
                break

        U[[i, max_row], :] = U[[max_row, i], :]
        P[[i, max_row], :] = P[[max_row, i], :]
        L[[i, max_row], :] = L[[max_row, i], :]

        permutation_vector[i], permutation_vector[max_row] \
            = permutation_vector[max_row], permutation_vector[i]

        L[i:n, i] = U[i:n, i] / U[i][i]

        l_temp = L[(i + 1):n, i]

        U[(i + 1):n, i:n] = U[(i + 1):n, i:n] - U[i, i:n] * l_temp[:, np.newaxis]

    for i in range(0, n):
        for j in range(i+1, n):
            U[j][i] = 0
            L[i][j] = 0

    np.fill_diagonal(L, 1)
    return P, L, U


a = np.random.rand(4, 4)
# a = np.array([[1., 2., 3.], [9., 8., 9.], [2., 3., 5.]])

print(a)

# L, U = scipy.linalg.lu(a, permute_l=True)

# print("L:", L)
# print("U:", U)
# print("L @ U:", L @ U)


P, L, U = lu_decomposition_with_pivoting(a)

# print("L:\n", L)
# print("U\n:", U)
# print("P:\n", P)
# print("L @ U:\n", L @ U)
# print("a: \n", a)
# print("P @ L @ U:\n", P @ L @ U)
# print("P @ L:\n", P @ L)
print("P @ A:\n", P @ a)
print("L @ U:\n", L @ U)
