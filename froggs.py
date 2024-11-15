import numpy as np
import random

def g(I):
    if(I.ndim == 2):
        xx = len(I[0])
        sum = np.zeros(len(I))
        for i in range(1, xx):
            sum = sum + I[:, i] / (xx - 1)
    if (I.ndim == 1):
        xx = len(I)
        sum = np.zeros(1)
        for i in range(1, xx):
            sum = sum + I[i] / (xx - 1)

    return 1 + 9 * sum
    

def f1(I):
    if(I.ndim == 2):
        return I[:, 0]
    if(I.ndim == 1):
        return I[0]

# ZDT1
def f2(I):
    if (I.ndim == 2):
        return g(I)*(1-I[:,0]/g(I)*I[:,0]/g(I))
    if (I.ndim == 1):
        return g(I)*(1-I[0]/g(I)*I[0]/g(I))


def Dominates(individual_1, individual_2):
    # Проверка, что individual_1 и individual_2 - это массивы (сектора)
    if isinstance(individual_1, np.ndarray) and isinstance(individual_2, np.ndarray):
        for i in range(len(individual_1)):  # Индексация массивов
            if individual_1[i] > individual_2[i]:
                return False
        return any(val_1 < val_2 for val_1, val_2 in zip(individual_1, individual_2))
    else:
        raise ValueError("individual_1 and individual_2 should be numpy arrays")

def non_dom_sort(I, flag):
    population1 = np.array([])
    I1 = np.array([])

    # Заполняем список `population` значениями функций f1 и f2
    population = np.vstack((f1(I), f2(I))).T

    while len(population)>0:
        c = 0

        for i in range(len(population)):
            c = 0
            for j in range(len(population)):
                if i != j and Dominates(population[j], population[i]):
                    c += 1

            if c == 0:
                population1 =np.append(population1,population[i])
                I1 = np.append(I1, I[i])


        # Удаление элементов из `population` и `I`, основываясь на `population1` и `I1`
        population = population[~np.isin(population, population1)].reshape(-1,2)
        I = I[~np.isin(I, I1)].reshape(-1,2)

        #print('result', ~np.isin(population, population1))
        #print(population)
        # Если флаг установлен, выводим и выходим из функции
        if flag:
            return I1.reshape(-1,2)
    return I1.reshape(-1,2)

def function(x):
    #return (x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2
    #return 100*np.sqrt(abs(x[1]-0.01*x[0]**2))+0.01*abs(x[0]+10)
    return (x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2

P = 200
iters = 100
it = 50
M = 20
C = 1.6
#a = np.array([-10,-10])
#b = np.array([10,10])
#a = np.array([-15, -3])
#b = np.array([-5, 3])
a = np.array([0, 0])
b = np.array([1, 1])
n = 2
x = np.random.uniform(a, b, (P,2))
# y = np.zeros(P,2)
# for i in range (P):
#     y[i,0] = f1(x[i])
#     y[i,1] = f2(x[i])
x = non_dom_sort(x,False)
best = random.choices(non_dom_sort(x,True))[0]
print(best)

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

for j in range(iters):
    for i in range(it):
        for group_idx, row in enumerate(x):
            
            row = non_dom_sort(x,False)
            worse = row[-1]
            best_row = best = random.choices(non_dom_sort(row,True))[0]
            
            # Применяем правила обновления
            #if function(calculate(worse, best_row, C, a, b)) < function(worse):
            if Dominates(np.array([f1(calculate(worse, best_row, C, a, b)),f2(calculate(worse, best_row, C, a, b))]),np.array([f1(worse),f2(worse)])): 
                worse = calculate(worse, best_row, C, a, b)
            elif Dominates(np.array([f1(calculate(worse, best, C, a, b)),f2(calculate(worse, best, C, a, b))]),np.array([f1(worse),f2(worse)])):
                worse = calculate(worse, best, C, a, b)
            else:
                worse = np.random.uniform(0, 1, 2)

            # Пересортируем строку после изменений
            row[-1] = worse

            # Сохраняем изменения в исходный массив
            x[group_idx] = row

    # Преобразуем массив обратно в одномерный и пересортируем
    x = np.concatenate(x)  # Преобразуем обратно в одномерный массив
    x = non_dom_sort(x,False)

    # Обновляем лучшее и худшее решение
    best = random.choices(non_dom_sort(x,True))[0]
    #worse = x[-1]

    # Снова распределяем элементы по группам
    x = distribute(x, M)
print(x.reshape(-1,2))
