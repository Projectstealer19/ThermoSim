from cycles.carnot import carnot_cycle
from utils.carnot_plot import plot_pv_diagram, plot_ts_diagram

Th = float(input("Enter hot reservoir temperature (K): "))
Tc = float(input("Enter cold reservoir temperature (K): "))
Qh = float(input("Enter heat supplied Qh (J): "))

results = carnot_cycle(Th, Tc, Qh)

if results is None:
    print("Invalid temperatures! Th must be greater than Tc.")
else:
    print("\n===== Carnot Cycle Results =====")
    print(f"Efficiency       : {results['efficiency']:.2f}%")
    print(f"Work Done        : {results['work_done']:.2f} J")
    print(f"Heat Rejected    : {results['heat_rejected']:.2f} J")
    print(f"Entropy Change   : {results['delta_s']:.2f} J/K")

    print("\nState Points:")
    for i in range(4):
        print(f"  State {i+1}: V = {results['V'][i]:.4f} m³  |  P = {results['P'][i]:.2f} Pa")

    plot_pv_diagram(results)
    plot_ts_diagram(results)