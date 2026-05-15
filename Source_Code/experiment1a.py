import matplotlib.pyplot as plt
from simulation import Simulation

# Dictionary of sidereal orbital periods from https://ssd.jpl.nasa.gov/planets/phys_par.html
nasa_periods = {
    "mercury": 0.2408467,
    "venus": 0.61519726,
    "earth": 1.0000174,
    "mars": 1.8808476,
    "jupiter": 11.862615
}

total_time = 12
num_steps = 12 * 16000 # 16000 intervals per year
sim = Simulation("parameters_solar.json", num_steps, total_time)

sim.beeman_compute()
sim.compute_cycles()
cycles = sim.return_cycles()

table_data = []

for planet, nasa_period in nasa_periods.items(): # For every key and value in the nasa_periods dictionary
    if planet in cycles: # if the planet exists in the cycles dictionary and has non-zero experimental orbital period
        sim_period = total_time / cycles[planet] # Calculate the experimental period by period = Time/Cycles
        abs_error = abs(sim_period - nasa_period) # Calculate absolute error between experimental and observational data
        pct_error = (abs_error / nasa_period) * 100 # Calculate percentage error pct_error
        
        # Add a list of data that will be used as a row to the table_data list that stores rows

        table_data.append([
            planet.capitalize(), 
            f"{sim_period:.6f}", # Fixed point truncation for neatness
            f"{nasa_period:.6f}", 
            f"{abs_error:.6f}", 
            f"{pct_error:.6f}%"
        ])


# Table generation and formatting
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight') # No excess white space
ax.axis('off') # Hide x and y axis

column_labels = ["Planet", "Simulated Period (yr)", "NASA Period (yr)", "Absolute Error (yr)", "Percentage Error"]
table = ax.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center') # Forces text to be at the centre
table.scale(1, 1.8)
table.auto_set_font_size(False)
table.set_fontsize(10)

plt.tight_layout()
plt.savefig("experiment1a.png", dpi=300, bbox_inches='tight')
plt.show()