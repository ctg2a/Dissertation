import numpy as np

def function(x):
    return (x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2

P = 100
iters = 50
it = 10
M = 5
C = 1.6
a = np.array([-10,-10])
b = np.array([10,10])
n = 2
x = np.random.uniform(a, b, (P,2))
y = np.zeros(P)
for i in range (P):
    y[i] = function(x[i])
x = x[np.argsort(y)]
best = x[0]
def calculate(worse, best, C, border_0, border_1):  
    sol = border_1+1
    rand = np.random.uniform(0, 1)
    
    while any((sol < border_0) | (sol > border_1)):
        rand = np.random.uniform(0, 1)
        sol = worse + C * rand * (best - worse)
    return sol

def distribute(x, M):
    groups = [[] for _ in range(M)]
    for i, x_i in enumerate(x):
        groups[i % M].append(x_i)
    # Преобразуем каждую группу в массив NumPy
    groups = [np.array(group) for group in groups]
    return np.array(groups, dtype=object)


x = distribute(x,M)
#print(x)

for j in range(iters):
    for i in range(it):
        for group_idx, row in enumerate(x):
            y_y = np.zeros(len(row))
            for k in range(len(row)):
                y_y[k] = function(row[k])
            # Сортируем строку row
            row = row[np.argsort(y_y)]
            worse = row[-1]
            best_row = row[0]

            # Применяем правила обновления
            if function(calculate(worse, best_row, C, a, b)) < function(worse):
                worse = calculate(worse, best_row, C, a, b)
            elif function(calculate(worse, best, C, a, b)) < function(worse):
                worse = calculate(worse, best, C, a, b)
            else:
                worse = np.random.uniform(0, 1, 2)

            # Пересортируем строку после изменений
            row[-1] = worse

            # Сохраняем изменения в исходный массив
            x[group_idx] = row

    # Преобразуем массив обратно в одномерный и пересортируем
    x = np.concatenate(x)  # Преобразуем обратно в одномерный массив
    y = np.zeros(P)
    for i in range(P):
        y[i] = function(x[i])
    x = x[np.argsort(y)]

    # Обновляем лучшее и худшее решение
    best = x[0]
    worse = x[-1]

    # Снова распределяем элементы по группам
    x = distribute(x, M)
print(best,function(best))
