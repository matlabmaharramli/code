import numpy as np
import matplotlib.pyplot as plt
from simulation import Simulation

nasa_periods = {
    "mercury": 0.2408467,
    "venus": 0.61519726,
    "earth": 1.0000174,
    "mars": 1.8808476,
    "jupiter": 11.862615
}

planet_list = list(nasa_periods.keys())
period_list = list(nasa_periods.values())


total_time = 12
resolutions = np.array([50, 100, 250, 500, 1000, 2000, 4000, 8000, 16000]) # steps per year

error_list = [] # will store numpy array for each planet, with numpy array containing resolution(first column) and corresponding absolute and percentage error



for planet in nasa_periods:
    error_list.append(np.zeros((resolutions.size, 3))) # Create a numpy array for each planet


for i in range(len(resolutions)):
    
    num_steps = total_time * resolutions[i] # Calculate num_steps based on the resolution
    sim = Simulation("parameters_solar.json", num_steps, total_time)
    
    # Run Simulation
    sim.beeman_compute()
    
    # Compute cycles
    sim.compute_cycles() 
    
    # Retrieve the dictionary containing the cycle counts
    exp_cycles = sim.return_cycles() 
    
    for j in range(len(planet_list)): # Iterate for every planet in the nasa_periods
        planet = planet_list[j] # Set currennt planet in the loop as planet
        
        # Check if the planet was successfully simulated and completed motion
        if (planet in exp_cycles) and (exp_cycles[planet] > 0):
            # Period = Total Simulation Time / Number of Laps completed
            
            simulated_period = total_time / exp_cycles[planet]
            nasa_p = nasa_periods[planet]
            
            # Calculate Absolute Error and Percentage Error
            absolute_error = abs(simulated_period - nasa_p)
            percentage_error = (absolute_error / nasa_p) * 100
            
            # Store resolution, absolute error, and percentage error in the j-th planet's 2D array
            error_list[j][i] = np.array([resolutions[i], absolute_error, percentage_error])



# Plotting the errors on a log-log scale + Formatting
plt.figure(figsize=(10, 6))

for j in range(len(planet_list)):
    planet_name = planet_list[j]
    
    # Extract data from numpy array structure
    # Column 2 is Resolution, Column 1 is Percentage Error
    res_vals = error_list[j][:, 0] 
    pct_errors = error_list[j][:, 2]
    
    # Only plot if we have data points (to avoid empty planet arrays)
    if len(res_vals) > 0:
        plt.plot(res_vals, pct_errors, marker='o', label=planet_name.capitalize())

# Plot on a log-log scale
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Resolution (steps/year)')
plt.ylabel('Percentage Error (%)')
plt.legend()
plt.grid(True, which="both", ls="--")

plt.tight_layout()
plt.savefig("experiment1b.png", dpi=300, bbox_inches='tight')
plt.show()

