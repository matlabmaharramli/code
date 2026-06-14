import numpy as np
import matplotlib.pyplot as plt
import os

def load_data():
    """Loads the pre-computed mathematical data from the math engine."""
    filename = "samovar_data.npz"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        print("Please run 'torricelli_math.py' first to generate the simulation data.")
        exit()
        
    data = np.load(filename)
    return data['h'], data['v'], data['t'], float(data['max_h'][0])

def run_simulation():
    H_DENSE, V_DENSE, T_DENSE, max_h = load_data()
    
    print("\n" + "="*50)
    print(" SAMOVAR DRAINAGE LIVE SIMULATION")
    print("="*50)

    # --- Phase 1: Set Initial State ---
    while True:
        try:
            init_str = input(f"\nEnter initial water level height [0 to {max_h:.2f} cm]: ")
            init_h = float(init_str)
            if 0 <= init_h <= max_h:
                break
            print("Value out of bounds.")
        except ValueError:
            print("Invalid number.")
            
    # Interpolate current state metrics based on the dense arrays
    current_h = init_h
    current_v = np.interp(current_h, H_DENSE, V_DENSE)
    current_t = np.interp(current_h, H_DENSE, T_DENSE) # Time elapsed from absolute top
    
    print(f"\n[Initial State] Height: {current_h:.2f} cm | Volume: {current_v:.2f} cm³")
    
    # --- Phase 2: Setup Dynamic Plot ---
    plt.ion() # Turn on interactive Matplotlib mode
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the full background curve
    ax.plot(T_DENSE, V_DENSE, color='steelblue', label="Full Drainage Profile", linewidth=2)
    
    # Create the dynamic point and text
    point, = ax.plot([current_t], [current_v], 'ro', markersize=10, zorder=5)
    state_text = ax.text(current_t + (T_DENSE[-1]*0.02), current_v, 
                         f"V: {current_v:.1f} cm³\nt: {current_t:.1f} s", 
                         verticalalignment='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title("Live Simulation: Volume vs Time", fontsize=14, fontweight='bold')
    ax.set_xlabel("Total Elapsed Time (t) [s]", fontsize=12)
    ax.set_ylabel("Remaining Volume (V) [cm³]", fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # --- Phase 3: Drainage Loop ---
    while current_v > 0.01: # Check slightly above 0 to prevent floating point infinite loops
        try:
            vol_input = input(f"\nRemaining Volume: {current_v:.2f} cm³. Enter ml (cm³) to pour (or 'q' to quit): ")
            if vol_input.lower() == 'q':
                break
            dv = float(vol_input)
            if dv <= 0:
                print("Please enter a positive amount.")
                continue
        except ValueError:
            print("Invalid input.")
            continue
            
        target_v = current_v - dv
        if target_v <= 0:
            dv = current_v
            target_v = 0
            print(f"\nPouring the last remaining {dv:.2f} cm³...")
        
        # Calculate new height and time seamlessly across piecewise breaks
        target_h = np.interp(target_v, V_DENSE, H_DENSE)
        target_t = np.interp(target_h, H_DENSE, T_DENSE)
        
        dt = target_t - current_t # Time just for this specific pour
        
        # Update metrics
        current_v = target_v
        current_h = target_h
        current_t = target_t
        
        print("-" * 50)
        print(f"POUR SUMMARY: Released {dv:.2f} cm³")
        print(f"Time taken for this pour: {dt:.2f} seconds.")
        print(f"NEW STATE: Height: {current_h:.2f} cm | Vol Left: {current_v:.2f} cm³ | Total Time: {current_t:.2f} s")
        
        # Update plot point dynamically
        point.set_data([current_t], [current_v])
        state_text.set_position((current_t + (T_DENSE[-1]*0.02), current_v))
        state_text.set_text(f"V: {current_v:.1f} cm³\nt: {current_t:.1f} s")
        fig.canvas.draw()
        fig.canvas.flush_events()
        
    print("\nTank Empty! Simulation Concluded.")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run_simulation()