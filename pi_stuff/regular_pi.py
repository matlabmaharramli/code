import numpy as np

def area(n):
    area = np.sin(2*np.pi/n)*n/2
    return area

print(area(1024))