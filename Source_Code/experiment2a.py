import numpy as np
import matplotlib.pyplot as plt
from simulation import Simulation

# Energy vs time for Beeman, Euler-Cromer, and Direct Euler Methods

params_file = "parameters_solar.json" # params file must contain body named 'sun'
total_time = 12 # in Earth Years
num_steps = 12 * 100 # 100 intervals per year

time_years = np.linspace(0, total_time, num_steps + 1) # Time array for plotting, from 0 to total_time with num_steps+1 points (including initial time)

# Run simulations for each method and compute total energy at each time step

sim_beeman = Simulation(params_file, num_steps, total_time)
sim_beeman.beeman_compute()
sim_beeman.compute_total_energy()
beeman = sim_beeman.return_energy() # Energy record for the Beeman Method

sim_euler_cromer = Simulation(params_file, num_steps, total_time)
sim_euler_cromer.euler_cromer_compute()
sim_euler_cromer.compute_total_energy()
euler_cromer = sim_euler_cromer.return_energy() # Energy record for the Euler-Cromer Method

sim_direct_euler = Simulation(params_file, num_steps, total_time)
sim_direct_euler.direct_euler_compute()
sim_direct_euler.compute_total_energy()
direct_euler = sim_direct_euler.return_energy() # Energy record for the Direct Euler Method

initial_energy = beeman[0] # Initial total energy from the Beeman simulation (same for all methods)


# Plotting and Formatting

i = 0.1 # Scaling factor for y-axis limits to focus on stable methods

# i = 0.1 # Too focus on Direct Euler
# i = 0.002 # High zoom factor to focus on stable methods
# i = 0.0004 # Higher zoom factor for energy plot, to better visualize the stable methods

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(time_years, direct_euler, 'b-', label='Direct Euler', linewidth=1.2)
ax.plot(time_years, euler_cromer, 'g-', label='Euler-Cromer', linewidth=1.2)
ax.plot(time_years, beeman, 'r-', label='Beeman', linewidth=1.2)

margin = abs(initial_energy) * i 
ax.set_ylim(initial_energy - margin, initial_energy + margin) # This forces the graph to focus around the initial energy, where stable methods will fluctuate.

ax.set_xlabel('Time (Earth Years)', fontsize=12)
ax.set_ylabel(r'Total Energy ($M_\oplus \cdot \text{AU}^2 \cdot \text{yr}^{-i2}$)', fontsize=12) # LaTeX
ax.legend(loc='lower left') # Legend positioned not to overlap with graphs
ax.grid(True, linestyle='--') # Grid to be shown

plt.tight_layout()
plt.savefig("experiment2a.png", dpi=300, bbox_inches='tight') # High resolution png file
plt.show()