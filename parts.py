
import numpy as np


def function(x):
    return (x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2


NP = 50
Nmin = 15
Nmax = 25
K = 100
omega = 0.5
alpha = 0.5
beta = 0.5
a = np.array([-10, -10])
b = np.array([10, 10])
v = np.zeros(NP)

x = np.random.uniform(a, b, (NP, 2))

best = np.copy(x)

for i in range(K):

    for j in range(NP):
        neighbour = np.random.randint(Nmin, Nmax+1)
        neighbours = []

        for _ in range(neighbour):
            neighbours.append(x[np.random.randint(0, NP)])
        y = np.zeros(neighbour)

        for i in range(neighbour):
            y[i] = function(neighbours[i])

        bestj = neighbours[np.argmin(y)]

        vj = omega*v[j]+alpha*(np.random.uniform(0, 1))*(best[j]-x[j]) \
            + omega*beta*(np.random.uniform(0, 1))*(bestj-x[j])

        if function(x[j]+vj) < function(x[j]):
            best[j] = x[j]+vj

        x[j] += vj
y = np.zeros(NP)

for i in range (NP):
    y[i] = function(x[i])
print(x[np.argmin(y)])
