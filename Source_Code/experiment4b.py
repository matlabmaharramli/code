import numpy as np
import matplotlib.pyplot as plt
from simulation import Simulation

# Visualizes times at which alignments occur

total_time = 1000 # Earth years, can be adjusted
resolution = 8000 # steps per year
num_steps = total_time * resolution
time_years = np.linspace(0, total_time, num_steps + 1) # Time array for plotting, from 0 to total_time with num_steps+1 points (including initial time)

threshold = 20 # Can be adjusted

# Run Simulation
sim = Simulation("parameters_solar.json", num_steps, total_time)
sim.beeman_compute()

sim.determine_alignment(threshold)
alignment_count = sim.return_alignment_count()
alignment_data = sim.return_alignment_data() # Returns a dictionary with keys as steps of ailgnment

# Convert to a set for instant lookups
alignment_steps_set = set(alignment_data.keys()) 

steps = np.linspace(0, num_steps, num_steps+1)

aligned_bool = np.array([s in alignment_steps_set for s in steps]) # True if step in steps is in alignment_steps, and False if not.

# Plotting and Formatting
plt.figure(figsize=(10, 6))
plt.plot(time_years, aligned_bool)
plt.xlabel("Time (Earth Years)")
plt.ylabel("Aligned (boolean)")
plt.tight_layout()
plt.savefig("experiment4b.png", dpi=300, bbox_inches='tight') # High Resolution
plt.show()