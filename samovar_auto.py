import numpy as np
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

def auto_pour_simulation():
    H_DENSE, V_DENSE, T_DENSE, max_h = load_data()
    
    print("\n" + "="*60)
    print(" AUTOMATED POUR SEQUENCE GENERATOR")
    print("="*60)

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
            
    # --- Phase 2: Define Pour Step ---
    while True:
        try:
            pour_str = input("Enter the amount of water to pour each time (in ml/cm³): ")
            pour_step = float(pour_str)
            if pour_step > 0:
                break
            print("Please enter a positive amount.")
        except ValueError:
            print("Invalid number.")

    # Interpolate starting metrics
    current_h = init_h
    current_v = float(np.interp(current_h, H_DENSE, V_DENSE))
    current_t = float(np.interp(current_h, H_DENSE, T_DENSE)) 
    
    print(f"\n[Starting State] Volume: {current_v:.2f} cm³ | Height: {current_h:.2f} cm")
    print("Generating pour sequence...\n")
    
    # --- Phase 3: Automated Pouring Loop ---
    pour_records = []
    pour_number = 1
    
    # We use 1e-4 instead of 0 to prevent microscopic floating-point infinite loops
    while current_v > 1e-4: 
        # Calculate how much we actually can pour
        actual_pour = min(pour_step, current_v)
        target_v = current_v - actual_pour
        
        # Ensure we clamp precisely to zero at the end
        if target_v <= 1e-4:
            target_v = 0
            
        # Interpolate new height and time
        target_h = float(np.interp(target_v, V_DENSE, H_DENSE))
        target_t = float(np.interp(target_h, H_DENSE, T_DENSE))
        
        dt = target_t - current_t # Time for this specific pour
        
        # Save to our array
        pour_records.append({
            "pour_num": pour_number,
            "amount": actual_pour,
            "time_taken": dt,
            "remaining_v": target_v
        })
        
        # Update metrics for next loop iteration
        current_v = target_v
        current_h = target_h
        current_t = target_t
        pour_number += 1

    # --- Phase 4: Print Results Table ---
    print(f"{'Pour #':<8} | {'Amount (cm³)':<15} | {'Time Taken (s)':<15} | {'Remaining (cm³)':<15}")
    print("-" * 65)
    
    total_pour_time = 0
    for record in pour_records:
        total_pour_time += record["time_taken"]
        print(f"{record['pour_num']:<8} | {record['amount']:<15.2f} | {record['time_taken']:<15.2f} | {record['remaining_v']:<15.2f}")
        
    print("-" * 65)
    print(f"Total time to empty tank:  {total_pour_time:.2f} seconds")
    print(f"Total number of pours:     {len(pour_records)}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    auto_pour_simulation()