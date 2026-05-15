import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

class Nuclei:
    
    def __init__(self, decay_constant, array_length):
        """
        Initializes the Nuclei object with a decay constant and a grid of nuclei.
        
        :param self:
        :param decay_constant: The decay constant of the nuclei
        :param array_length: The length of the square grid of nuclei
        """
        self.decay_constant = decay_constant
        self.array_length = array_length
        self.nuclei_grid = np.ones((array_length, array_length), dtype = np.int32)

    def simulate(self, time_step, series):
        """
        Simulates the decay of nuclei over a specified series.
        
        :param self:
        :param time_step: time step for the simulation
        :param series: number of half-lives to simulate
        """
        time_elapsed = 0.0
        element_count = self.array_length * self.array_length
        final_count = element_count / (2**series)
        decay_probability = self.decay_constant * time_step
        
        isFinished = False

        while not(isFinished):
               time_elapsed = time_elapsed + time_step
               for i in range(self.array_length):
                for j in range(self.array_length):
                    if self.nuclei_grid[i][j] !=0:
                        random_value = np.random.rand()
                        if decay_probability > random_value:
                            element_count = element_count - 1
                            self.nuclei_grid[i][j] = 0
                            if element_count <= final_count:
                                isFinished = True
                                break
                if element_count <= final_count:
                    break
        print(f"Simulation successful. Changes made to the original grid.\nInitial element count was {self.array_length * self.array_length} and final element count is {element_count}.\nTime elapsed to complete the series: {time_elapsed} minutes.")


    def simulate_half_life(self, time_step):
        """
        Simulates the decay of nuclei for one half-life (1 series).
        
        :param self:
        :param time_step: time step for the simulation
        """
        self.simulate(time_step, 1)
        print(f"Theoretical half-life: {np.log(2)/self.decay_constant} minutes.")
    
    def __str__(self):
        """
        Returns a string representation of the nuclei grid.
        
        :param self:
        """
        output = ""
        for i in range(self.array_length):
            for j in range(self.array_length):
                output += str(self.nuclei_grid[i][j]) + " "
            output += "\n"
        return output

    
    def plot_nuclei(self):
        """
        Plots the current state of the nuclei grid visually using Matplotlib.
        
        :param self:
        """

        r = 0.5
        fig, ax = plt.subplots()
        n = self.array_length
        for i in range(n):
            for j in range(n):
                if self.nuclei_grid[i][j] == 1:
                    x = j + 1
                    y = n - i
                    ax.add_patch(patches.Circle((x, y), r, color="r"))
        ax.set_xlim(0.5, n + 0.5)
        ax.set_ylim(0.5, n + 0.5)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()
