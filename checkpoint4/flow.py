import numpy as np
import matplotlib.pyplot as plt
from traffic import Traffic

# --- EXPERIMENT: Fundamental Diagram ---

densities = np.linspace(0, 1, 50)  # Test 50 different densities from 0% to 100%
flows = []

for d in densities:
    # Run a simulation for this specific density
    # We use a large N and niter to let the traffic reach a "steady state"
    sim = Traffic(N=100, niter=100, density=d)
    
    # Calculate the steady-state velocity
    steady_state_v = sim.avg_v[-1]
    
    # Calculate Flow: J = density * velocity
    flow = d * steady_state_v
    flows.append(flow)

# Plotting the results
plt.figure(figsize=(8, 5))
plt.plot(densities, flows, 'o-', color='crimson')
plt.title("The Fundamental Diagram of Traffic Flow")
plt.xlabel("Density (Cars per Cell)")
plt.ylabel("Flow (Cars per Iteration)")
plt.grid(True)
plt.show()