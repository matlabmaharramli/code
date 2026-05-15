from mandelbrot import Mandelbrot

class Julia(Mandelbrot):

    def __init__(self, c, N = 512, x_min = -1.5, x_max = 1.5, y_min = -1.5, y_max = 1.5, color_bar = False, interpolation = "none"):
        super().__init__(N, x_min, x_max, y_min, y_max, color_bar, interpolation)
        self.c = c
    
    def compute_n(self, z_n):
        """
        Computes the number of iterations before divergence for complex numbers c and z. n = 255 implies convergence.
    
        :param self:
        :param z_n: Complex number to compute iterations for
        :return: Number of iterations before divergence
        """
        n = 0
        while((n<255) and (abs(z_n)<2)):
            z_n = z_n**2 + self.c
            n += 1
        return n
