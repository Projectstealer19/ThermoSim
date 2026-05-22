
from cycles.brayton import brayton_cycle
from utils.brayton_plot import plot_ts_diagram
from analysis.brayton_eff_vs_pr import plot_efficiency_vs_rp

T1 = float(input("Enter compressor inlet temperature T1 (K): "))

T3 = float(input("Enter turbine inlet temperature T3 (K): "))

rp = float(input("Enter pressure ratio rp: "))

gamma = float(input("Enter gamma (Cp/Cv): "))

# Run Brayton Simulation

results = brayton_cycle(T1, T3, rp, gamma)

print("\n===== Brayton Cycle Results =====")

print(f"\nT1 = {results['T1']:.2f} K")

print(f"T2 = {results['T2']:.2f} K")

print(f"T3 = {results['T3']:.2f} K")

print(f"T4 = {results['T4']:.2f} K")

print(f"\nThermal Efficiency = {results['efficiency']:.2f}%")

# Plot T-S Diagram

plot_ts_diagram(
    results['T1'],
    results['T2'],
    results['T3'],
    results['T4'],
    gamma
)
plot_efficiency_vs_rp(gamma)