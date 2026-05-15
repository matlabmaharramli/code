import numpy as np
import matplotlib.pyplot as plt
import time

class Mandelbrot:

    def __init__(self, N = 512, x_min = -2.025, x_max = 0.6, y_min = -1.125, y_max = 1.125, color_bar = False, interpolation = "none"):
        self.N = N
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.color_bar = color_bar
        self.interpolation = interpolation
        self.exec_time = 0

    def create_grid(self):
        """
        Creates a grid of complex numbers based on the range of x and y values.
        
        :param self:
        :return: Meshgrid arrays XX, YY and complex grid ZZ
        """
        X = np.linspace(self.x_min, self.x_max, self.N)
        Y = np.linspace(self.y_min, self.y_max, self.N)
        XX, YY = np.meshgrid(X, Y)
        ZZ = XX + YY * 1j
        return XX, YY, ZZ

    def compute_n(self, c):
        """
        Computes the number of iterations before divergence for complex numbers c and z. n = 255 implies convergence.
    
        :param self:
        :param c: Complex number to compute iterations for
        :return: Number of iterations before divergence
        """
        z_n = 0
        n = 0
        while((n<255) and (abs(z_n)<2)):
            z_n = z_n**2 + c
            n += 1
        return n

    def compute(self):
    
        time1 = time.time()

        vectorized_compute_n = np.vectorize(self.compute_n)
        XX, YY, ZZ = self.create_grid()
        nn = vectorized_compute_n(ZZ)

        plt.imshow(
            nn,
            extent=(XX.min(), XX.max(), YY.min(), YY.max()),
            origin="lower",
            cmap="turbo",
            aspect="equal",
            interpolation=self.interpolation
        )

        if self.color_bar:
            plt.colorbar()

        time2 = time.time()
        self.exec_time = time2 - time1

        plt.show()