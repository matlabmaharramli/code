import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Added 'x' as a dummy variable for proper definite integration
h, t, x = sp.symbols("h t x")

outer_r_list = []
inner_r_list = []

# Units: seconds, centimeters
# Physics Settings ------------------------------------------------------------
g = 981
outlet_area = 4
c = 0.6

ground_h = 0
max_h = 20.4

outer_r_list.append(-3.41471 / (h + 1.12285) + 9.65949)
outer_r_list.append(-0.03127 * h**3 + 1.77287 * h**2 - 32.99845 * h + 211.4001)

inner_r_list.append(5)
inner_r_list.append(-(1.75 / 2.285) * (h - 15.715) + 5)
inner_r_list.append(3.25)

# Physics settings end ---------------------------------------------------------

# --- Find Break Points ---
outer_break_points = []
for i in range(len(outer_r_list)-1):
    expr = outer_r_list[i+1] - outer_r_list[i]
    solutions = sp.solve(expr, h)
    
    positive_real_solutions = []
    for sol in solutions:
        val = sol.evalf()
        if abs(sp.im(val)) < 1e-5 and sp.re(val) > 0:
            positive_real_solutions.append(sp.re(val))

    break_point = min(positive_real_solutions)
    outer_break_points.append(break_point)

inner_break_points = []
for i in range(len(inner_r_list)-1):
    expr = inner_r_list[i+1] - inner_r_list[i]
    solutions = sp.solve(expr, h)
    
    positive_real_solutions = []
    for sol in solutions:
        val = sol.evalf()
        if abs(sp.im(val)) < 1e-5 and sp.re(val) > 0:
            positive_real_solutions.append(sp.re(val))
            
    break_point = min(positive_real_solutions)
    inner_break_points.append(break_point)

combined_break_points = outer_break_points.copy()
for new_point in inner_break_points:
    unique = True
    for point in combined_break_points:
        if abs(point - new_point) < 1e-5:
            unique = False
    if unique:
        combined_break_points.append(new_point)
    
combined_break_points.sort()

section_intervals = combined_break_points.copy()
section_intervals.insert(0, ground_h)
section_intervals.append(max_h)

cross_sections = []
j, k = 0, 0
for i in range(1, len(section_intervals)):
    area = sp.pi * ((outer_r_list[j])**2 - (inner_r_list[k])**2)
    cross_sections.append(area)

    for point in outer_break_points:
        if abs(section_intervals[i] - point) < 1e-5:
            j += 1
    
    for point in inner_break_points:
        if abs(section_intervals[i] - point) < 1e-5:
            k += 1

# --- Physics & Torricelli Calculation ---
k_val = c * outlet_area * sp.sqrt(2*g)

time_functions = []
reversed_sections = cross_sections[::-1]
reversed_intervals = section_intervals[::-1]

for i in range(len(reversed_sections)):
    expr_x = reversed_sections[i].subs(h, x)
    integrand_x = -expr_x / (k_val * sp.sqrt(x))
    
    if i == 0:
        boundary_h = max_h
        boundary_t_value = 0
    else:
        boundary_h = reversed_intervals[i]
        boundary_t_value = float(time_functions[i-1].subs(h, boundary_h).evalf())
        
    time_expr = boundary_t_value + sp.Integral(integrand_x, (x, boundary_h, h))
    time_functions.append(time_expr.doit())

time_functions.reverse()

# --- Volume Calculation ---
volume_functions = []
current_volume = 0

for i in range(len(cross_sections)):
    lower_h = section_intervals[i]
    expr_x = cross_sections[i].subs(h, x)
    
    vol_expr = current_volume + sp.Integral(expr_x, (x, lower_h, h))
    vol_evaluated = vol_expr.doit()
    
    volume_functions.append(vol_evaluated)
    current_volume = float(vol_evaluated.subs(h, section_intervals[i+1]).evalf())


# --- Plotting Helpers and Functions ---

def format_latex(expr):
    """Rounds SymPy expressions to 4 decimals and converts to a Matplotlib-safe LaTeX string."""
    expr = sp.sympify(expr) 
    rounded_expr = expr.xreplace({n: sp.Float(np.round(float(n), 4)) for n in expr.atoms(sp.Float)})
    latex_str = sp.latex(rounded_expr)
    
    latex_str = latex_str.replace(r"\left(", "(").replace(r"\right)", ")")
    latex_str = latex_str.replace(r"\left[", "[").replace(r"\right]", "]")
    latex_str = latex_str.replace(r"\limits", "")
    latex_str = latex_str.replace(r"\,", " ") 
    
    return f"${latex_str}$"

def evaluate_array(expr, h_array):
    """Safely evaluates a SymPy expression over a numpy array."""
    expr = sp.sympify(expr)
    try:
        if expr.has(sp.Integral):
            raise ValueError("Expression contains an unevaluated integral")
        func = sp.lambdify(h, expr, modules="numpy")
        res = func(h_array)
        if np.isscalar(res):
            return np.full_like(h_array, float(res))
        return res
    except Exception:
        evaluated = []
        for val in h_array:
            numeric_val = complex(expr.subs(h, val).evalf())
            evaluated.append(numeric_val.real)
        return np.array(evaluated)

def plotHR():
    plt.figure(figsize=(8, 8))
    
    outer_bounds = [ground_h] + outer_break_points + [max_h]
    for i in range(len(outer_r_list)):
        start_h = float(outer_bounds[i])
        end_h = float(outer_bounds[i+1])
        h_array = np.linspace(start_h, end_h, 50)
        r_array = evaluate_array(outer_r_list[i], h_array)
            
        latex_eq = format_latex(outer_r_list[i])
        plt.plot(h_array, r_array, label=f"Outer {i+1} [{start_h:.1f}-{end_h:.1f}] $r(h) = $ {latex_eq}", linewidth=2)
        plt.scatter([start_h, end_h], [r_array[0], r_array[-1]], color='red', zorder=5)

    inner_bounds = [ground_h] + inner_break_points + [max_h]
    for i in range(len(inner_r_list)):
        start_h = float(inner_bounds[i])
        end_h = float(inner_bounds[i+1])
        h_array = np.linspace(start_h, end_h, 50)
        r_array = evaluate_array(inner_r_list[i], h_array)
            
        latex_eq = format_latex(inner_r_list[i])
        plt.plot(h_array, r_array, linestyle="--", label=f"Inner {i+1} [{start_h:.1f}-{end_h:.1f}] $r(h) = $ {latex_eq}", linewidth=2)
        plt.scatter([start_h, end_h], [r_array[0], r_array[-1]], color='blue', zorder=5)

    plt.title("Radius vs Height", fontsize=14, fontweight='bold')
    plt.xlabel("Height ($h$) [cm]", fontsize=12)
    plt.ylabel("Radius ($r$) [cm]", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=10)
    plt.subplots_adjust(bottom=0.35) 
    plt.show()

def plotTH():
    plt.figure(figsize=(8, 8))
    
    for i in range(len(time_functions)):
        start_h = float(section_intervals[i])
        end_h = float(section_intervals[i+1])
        h_array = np.linspace(start_h, end_h, 50)
        
        t_array = evaluate_array(time_functions[i], h_array)
        
        latex_eq_t = format_latex(time_functions[i])
        # Changed to represent Parametric Equation
        plt.plot(t_array, h_array, label=f"Sec {i+1} [{start_h:.1f}-{end_h:.1f}] Parametric: $(t(h), h)$ \n$t(h) = $ {latex_eq_t}", linewidth=2)
        plt.scatter([t_array[0], t_array[-1]], [h_array[0], h_array[-1]], color='black', zorder=5)

    plt.title("Height vs Time (Drainage Profile)", fontsize=14, fontweight='bold')
    plt.xlabel("Time ($t$) [s]", fontsize=12)
    plt.ylabel("Height ($h$) [cm]", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=10)
    plt.subplots_adjust(bottom=0.35)
    plt.show()

def plotTV():
    plt.figure(figsize=(8, 8))
    
    for i in range(len(time_functions)):
        start_h = float(section_intervals[i])
        end_h = float(section_intervals[i+1])
        h_array = np.linspace(start_h, end_h, 50)
        
        t_array = evaluate_array(time_functions[i], h_array)
        v_array = evaluate_array(volume_functions[i], h_array)
            
        latex_eq_v = format_latex(volume_functions[i])
        latex_eq_t = format_latex(time_functions[i])
        
        # Changed to represent Parametric Equation (since direct V(t) isn't analytically possible)
        plt.plot(t_array, v_array, label=f"Sec {i+1} [{start_h:.1f}-{end_h:.1f}] Parametric: $(t(h), V(h))$\n$V(h) = $ {latex_eq_v}\n$t(h) = $ {latex_eq_t}", linewidth=2)
        plt.scatter([t_array[0], t_array[-1]], [v_array[0], v_array[-1]], color='black', zorder=5)

    plt.title("Volume vs Time (Drainage Profile)", fontsize=14, fontweight='bold')
    plt.xlabel("Time ($t$) [s]", fontsize=12)
    plt.ylabel("Volume ($V$) [cm³]", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=10)
    plt.subplots_adjust(bottom=0.35)
    plt.show()

# --- Export Data for Simulation ---
def save():
    """Generates dense data arrays and exports them for the live simulation file."""
    print("\nGenerating numerical arrays for live simulation...")
    H_DENSE, V_DENSE, T_DENSE = [], [], []
    
    # 200 points per piece gives hyper-smooth interpolation for the UI
    for i in range(len(volume_functions)):
        start_h = float(section_intervals[i])
        end_h = float(section_intervals[i+1])
        h_arr = np.linspace(start_h, end_h, 200) 
        
        v_arr = evaluate_array(volume_functions[i], h_arr)
        t_arr = evaluate_array(time_functions[i], h_arr)
        
        if i < len(volume_functions) - 1:
            H_DENSE.extend(h_arr[:-1])
            V_DENSE.extend(v_arr[:-1])
            T_DENSE.extend(t_arr[:-1])
        else:
            H_DENSE.extend(h_arr)
            V_DENSE.extend(v_arr)
            T_DENSE.extend(t_arr)

    # Save everything into a compressed Numpy format
    np.savez("samovar_data.npz", 
             h=np.array(H_DENSE), 
             v=np.array(V_DENSE), 
             t=np.array(T_DENSE), 
             max_h=np.array([max_h]))
    print("Export Complete! Data saved to 'samovar_data.npz'.")

# --- Execution ---
if __name__ == "__main__":
    print("Rendering static mathematical plots...")
    plotHR()
    plotTH()
    plotTV()
    
    # Save the data after plots are closed
    save()