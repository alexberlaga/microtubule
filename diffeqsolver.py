import numpy as np
import matplotlib.pyplot as plt

N = 13
U = 0.05
W = 0.05

def laplace(s):
    mat = np.zeros((N + 1, N + 1))
    for i in range(N):
        mat[i][i] = -1 * (s + i * U + (N - i) * W)
        mat[i][i - 1] = (N - i + 1) * W
        mat[i][i + 1] = (i + 1) * U
    mat[N][N - 1] = N * U
    b = np.zeros(N + 1)
    b[N] = 1
    x = np.linalg.solve(mat, b)
    return x

sols = []
for i in range(N + 1):
    sols.append([])
for s in range(10000):
    sol = laplace(0.01 * s)
    for i in range(N + 1):
        sols[i].append(sol[i])


x_axis = [0.01 * x for x in range(10000)]
for sol in sols:
    plt.plot(x_axis, sol)
plt.show()

