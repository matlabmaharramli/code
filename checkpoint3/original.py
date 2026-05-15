import numpy as np
import matplotlib.pyplot as plt
import time

def create_grid(N = 512, x_min = -2.025, x_max = 0.6, y_min = -1.125, y_max = 1.125):
    """
    Creates a grid of complex numbers based on the specified range of x and y values.
    
    :param N: Number of points along each axis
    :param x_min: Minimum x value
    :param x_max: Maximum x value
    :param y_min: Minimum y value
    :param y_max: Maximum y value
    :return: Meshgrid arrays XX, YY and complex grid ZZ
    """
    X = np.linspace(x_min, x_max, N)
    Y = np.linspace(y_min, y_max, N)
    XX, YY = np.meshgrid(X, Y)
    ZZ = XX + YY * 1j
    return XX, YY, ZZ

def compute_n(C = 0 + 0j, z_n = 0 + 0j):
    """
    Computes the number of iterations before divergence for a given complex numbers C and z_n. n = 255 implies convergence.
    
    :param z_n: Initial complex number
    :param C: Complex number
    :return: Number of iterations before divergence
    """
    n = 0
    while((n<255) and (abs(z_n)<2)):
        z_n = z_n**2 + C
        n += 1
    return n

def main():
    
    time1 = time.time()

    vectorized_compute_n = np.vectorize(compute_n)
    XX, YY, ZZ = create_grid()
    nn = vectorized_compute_n(ZZ)

    plt.imshow(
        nn,
        extent=(XX.min(), XX.max(), YY.min(), YY.max()),
        origin="lower",
        cmap="turbo",
        aspect="equal",
        interpolation="none"
    )

    # plt.colorbar()

    time2 = time.time()
    print(f"Computation took {time2-time1} seconds")

    plt.show()

if __name__ == "__main__":
    main()