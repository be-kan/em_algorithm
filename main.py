import numpy as np
import matplotlib.pyplot as p
import sys
from scipy.stats import norm

# 標本を生成
n = 1000
x = np.random.randn(n) + (np.random.rand(n) > 0.3) * 4 - 2


# 負担率（隠れ関数）を求める
def calc_responsibility(x, w, u, σ):
    responsibility = []

    for i in range(2):
        responsibility.append(w[i] * np.exp(-0.5 * (x - u[i]) ** 2 / σ[i]) / np.sqrt(2 * np.pi * σ[i]))

    return responsibility / sum(responsibility)


# パラメータを更新
def calc_parameters(x, responsibility):
    N = []
    new_u = []
    new_σ = []
    new_w = []

    for i in range(2):
        N.append(sum(responsibility[i]))

        new_w.append(N[i] / x.size)

        u_total = 0
        for j in range(x.size):
            u_total += responsibility[i][j] * x[j]
        new_u.append(u_total / N[i])

        σ_total = 0
        for j in range(x.size):
            σ_total += responsibility[i][j] * ((x[j] - u[i]) ** 2)
        new_σ.append(σ_total / N[i])

    return (new_w, new_u, new_σ)


# Q関数を求める
def calc_Q(x, w, u, σ, responsibility):
    Q = 0
    for i in range(x.size):
        for j in range(2):
            Q += res[j][i] * np.log(w[j] * np.exp(-0.5 * ((x[i] - u[j]) ** 2) / σ[j]) / np.sqrt(2 * np.pi * σ[j]))

    return Q


if __name__ == '__main__':
    w = [0.5, 0.5]
    u = [-1, 1]
    σ = [1, 2]
    epsilon = 0.0001
    delta = 1
    Q = -sys.float_info.max
    count = 0

    # Q関数の変化が閾値を下回るまでパラメータを更新
    while delta > epsilon:
        res = calc_responsibility(x, w, u, σ)
        w, u, σ = calc_parameters(x, res)
        new_Q = calc_Q(x, w, u, σ, res)
        delta = new_Q - Q
        Q = new_Q
        count += 1

    print(str(count) + "回ループ")
    print(w)
    print(u)
    print(σ)
