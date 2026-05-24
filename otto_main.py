from cycles.otto import otto_cycle
from utils.otto_plot import plot_otto_ts

# ------------------------------------------------
# USER INPUTS
# ------------------------------------------------

T1 = float(input("Enter initial temperature T1 (K): "))

r = float(input("Enter compression ratio r: "))

T3 = float(input("Enter maximum cycle temperature T3 (K): "))

gamma = float(input("Enter gamma (Cp/Cv): "))

# ------------------------------------------------
# RUN OTTO CYCLE
# ------------------------------------------------

results = otto_cycle(T1, r, T3, gamma)

# ------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------

print("\n===== Otto Cycle Results =====")

print(f"\nT1 = {results['T'][0]:.2f} K")
print(f"T2 = {results['T'][1]:.2f} K")
print(f"T3 = {results['T'][2]:.2f} K")
print(f"T4 = {results['T'][3]:.2f} K")

print(f"\nHeat Added     = {results['Q_in']:.2f} J/kg")

print(f"Heat Rejected  = {results['Q_out']:.2f} J/kg")

print(f"Net Work       = {results['W_net']:.2f} J/kg")

print(f"Efficiency     = {results['efficiency']:.2f}%")

# ------------------------------------------------
# PLOT T-S DIAGRAM
# ------------------------------------------------

plot_otto_ts(
    results["T"],
    results["S"]
)