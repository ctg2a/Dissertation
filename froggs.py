import numpy as np


def function(x):
    return (x[:,0]+2*x[:,1]-7)**2+(2*x[:,0]+x[:,1]-5)**2


def distribute(x, M):
    groups = [[] for _ in range(M)]
    for i, x_i in enumerate(x):
        groups[i % M].append(x_i)
    # Преобразуем каждую группу в массив NumPy
    groups = [np.array(group) for group in groups]
    return np.array(groups, dtype=object)


def calculate(worse, best, C, border_0, border_1):
    sol = border_1+1
    while (sol > border_1 or sol < border_0):
        rand = np.random.uniform(0, 1)
        sol = worse + C * rand * (best - worse)
    return sol


P = 20
iters = 20
it = 5
M = 5
C = 1.6
a = 0
b = 1
n = 2


x = np.random.uniform(a, b, (P,2))
x = x[np.argsort(function(x))]
best = x[0]
x = distribute(x, M)

for j in range(iters):

    for i in range(it):
        for row in x:
        

            # Найдем худший и лучший элементы в row
            worse = row[np.argsort(function(row))][-1]
            best_row = row[np.argsort(function(row))][0]
            rand = np.random.uniform(0, 1)

            # Применяем правила обновления
            if function(calculate(worse, best_row, C, a, b)) > function(worse):
                row[np.argsort(function(row))
                    ][-1] = calculate(worse, best_row, C, a, b)
            elif function(calculate(worse, best, C, a, b)) > function(worse):
                row[np.argsort(function(row))
                    ][-1] = calculate(worse, best, C, a, b)
            else:
                row[np.argsort(function(row))][-1] = np.random.uniform(0, 1)

            # Пересортируем строку после изменений
            row = row[np.argsort(function(row))]

    # Преобразуем массив обратно в одномерный и пересортируем
    x = np.concatenate(x)  # Преобразуем в одномерный массив
    x = x[np.argsort(function(x))]
    best = x[0]
    # Снова распределяем элементы по группам
    x = distribute(x, M)

print('best =', best)
