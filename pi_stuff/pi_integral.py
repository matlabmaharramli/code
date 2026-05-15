import numpy as np

def semi_circle(x):
    y = np.sqrt(1-(x**2)) #valid for -1<x<1
    return y

def area(function, N, a, b):
    area = 0
    dx = (b-a)/N
    for i in range(N):
        area = area + function(a+i*dx)*dx
    return area

pi = 2*(area(semi_circle, 2048, -1, 1))
print(pi)