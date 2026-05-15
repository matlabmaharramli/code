import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Traffic:
    
    def __init__(self, N, niter, density):
        """
        Initializes the traffic simulation.
        
        :param N: number of cells
        :param niter: number of iterations
        :param density: car density (fraction of cells that have a car on them)
        """
        self.N = N
        self.niter = niter
        self.density = density
        self.c = np.empty((self.niter, self.N), dtype=np.int8) #creates 2D array to be changed to 0's and 1's during computation
        self.v = np.full((self.niter-1, self.N), 2, dtype=np.int8) #creates 2D array of 2's (elements without cars will remain at 2, elements with moving cars will be set to 1, elements without moving cars will be set to 0)
        self.compute()
        self.avg_v = self.compute_avg_v()
    

    #METHODS THAT ARE NOT INTENDED FOR USE AFTER INSTANTIATION

    def compute(self):

        #generates traffic state at (0)th timestep based on car density
        #calculate the number of cars
        num_cars = int(self.N * self.density)
        
        #create the first row: number of 1s followed by 0s
        first_row = np.zeros(self.N, dtype=np.int8)
        first_row[:num_cars] = 1
        
        #shuffle it so the starting positions are random
        np.random.shuffle(first_row)
        self.c[0] = first_row
        
        #computes traffic state at each subsequent timestep based on traffic state at previous timestep and rules of the simulation
        for n in range(self.niter-1):
            for j in range(self.N):
                b = self.c[n][(j-1)%self.N] #(j-1)th element
                c = self.c[n][j] #(j)th element
                f = self.c[n][(j+1)%self.N] #(j+1)th element

                if c == 1: #element contains a vehicle
                    if f == 1:
                        self.c[n+1][j] = 1
                        self.v[n][j] = 0 #vehicle at element has not moved (v set to 0)
                    else:
                        self.c[n+1][j] = 0
                        self.v[n][j] = 1 #vehicle at element has moved (v set to 1)
                elif c == 0: #element does not contain a vehicle
                    if b == 1:
                        self.c[n+1][j] = 1
                    else:
                        self.c[n+1][j] = 0

    def compute_avg_v(self):
        avg_v = np.empty((self.niter-1))

        for n in range(self.niter-1):
            n_moving = 0
            n_total = 0
            for v in self.v[n]:
                if v == 1:
                    n_total += 1
                    n_moving += 1
                if v == 0:
                    n_total += 1
            try:
                avg_v[n] = n_moving/n_total
            except ZeroDivisionError:
                avg_v[n] = 0
        return avg_v
    

    #METHODS THAT COULD BE IMPLEMENTED AFTER INSTANTIATION FOR GRAPHICAL PRESENTATION OF DATA

    def display(self):
        plt.imshow(self.c, cmap = 'binary', interpolation = 'none')
        plt.show()


    def simulate(self):
        fig, ax = plt.subplots()
        ax.set_yticks([])
        im = ax.imshow(self.c[0:1, :], cmap = 'binary', animated = True)

        def animate(frame):
            im.set_data(self.c[frame:frame+1, :])
            return im,
        
        animation = FuncAnimation(fig, animate, frames = self.niter, interval = 1000, blit = True, repeat = False)
        plt.show()

    def plot_avg_v(self):
        plt.plot(np.arange(self.niter-1), self.avg_v)
        plt.gca().set_xlabel('Average Velocity')
        plt.gca().set_ylabel('Iteration')
        plt.show()