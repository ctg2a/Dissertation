import numpy as np

def function(x):
    return (x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2

NP = 30
Nmin = 15
Nmax = 25
K = 100
omega = 0.5
alpha = 0.5
beta = 0.5
a = np.array([-10,-10])
b = np.array([10,10])
v = np.zeors(NP)

x = np.random.uniform(a, b, (NP,2))


