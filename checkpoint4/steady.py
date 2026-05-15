import numpy as np
import matplotlib.pyplot as plt
from traffic import Traffic

densities = np.linspace(0, 1, 50)  # Test 50 different densities from 0% to 100%
steady_states = []

for d in densities:
    # Run a simulation for this specific density
    # We use a large N and niter to let the traffic reach a "steady state"
    sim = Traffic(N=100, niter=100, density=d)
    
    # Calculate the steady-state velocity
    steady_state_v = sim.avg_v[-1]
    steady_states.append(steady_state_v)

# Plotting the results
plt.figure(figsize=(8, 5))
plt.plot(densities, steady_states, 'o-', color='crimson')
plt.title("")
plt.xlabel("Density (Cars per Cell)")
plt.ylabel("Steady State")
plt.grid(True)
plt.show()