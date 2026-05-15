import numpy as np
import matplotlib.pyplot as plt
from simulation import Simulation

# Threshold vs Frequency of Alignment

total_time = 1000 # Earth years, can be adjusted
resolution = 8000 # steps per year
num_steps = total_time * resolution

thresholds = np.linspace(1, 20, 20)

alignment_counts = []

# Run Simulation
sim = Simulation("parameters_solar.json", num_steps, total_time)
sim.beeman_compute()

for threshold in thresholds:
    # determine_alignment method is reusable and can be called multiple times with different thresholds without the need to rerun the simulation.
    sim.determine_alignment(threshold)
    alignment_count = sim.return_alignment_count()
    alignment_counts.append(alignment_count)


# Plotting and Formatting

plt.figure(figsize=(10, 6))
plt.plot(thresholds, alignment_counts, marker='o')
plt.xlabel("Alignment Threshold (degrees)")
plt.ylabel("Frequency of Alignment")
plt.tight_layout()
plt.savefig("experiment4a.png", dpi=300, bbox_inches='tight') # High Resolution
plt.show()






