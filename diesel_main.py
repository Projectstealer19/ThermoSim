from cycles.diesel import diesel_cycle
from utils.diesel_plot import plot_diesel_ts

# ------------------------------------------------
# USER INPUTS
# ------------------------------------------------

T1 = float(input("Enter initial temperature T1 (K): "))

r = float(input("Enter compression ratio r: "))

rc = float(input("Enter cut-off ratio rc: "))

gamma = float(input("Enter gamma (Cp/Cv): "))

# ------------------------------------------------
# RUN DIESEL CYCLE
# ------------------------------------------------

results = diesel_cycle(T1, r, rc, gamma)

# ------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------

print("\n===== Diesel Cycle Results =====")

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

plot_diesel_ts(
    results["T"],
    results["S"]
)