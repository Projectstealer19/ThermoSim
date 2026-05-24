from cycles.refrigerator import refrigeration_cycle
from utils.refrigerator_plot import plot_refrigeration_ts

# ------------------------------------------------
# USER INPUTS
# ------------------------------------------------

T_evap = float(input("Enter evaporator temperature (K): "))

T_cond = float(input("Enter condenser temperature (K): "))

eta_comp = float(input("Enter compressor efficiency (0-1): "))

# ------------------------------------------------
# RUN REFRIGERATION CYCLE
# ------------------------------------------------

results = refrigeration_cycle(
    T_evap,
    T_cond,
    eta_comp
)

# ------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------

print("\n===== Refrigeration Cycle Results =====")

print("\nTemperatures:")

print(f"T1 = {results['T'][0]:.2f} K")

print(f"T2 = {results['T'][1]:.2f} K")

print(f"T3 = {results['T'][2]:.2f} K")

print(f"T4 = {results['T'][3]:.2f} K")

print("\nEnthalpies:")

print(f"H1 = {results['H'][0]:.2f} J/kg")

print(f"H2 = {results['H'][1]:.2f} J/kg")

print(f"H3 = {results['H'][2]:.2f} J/kg")

print(f"H4 = {results['H'][3]:.2f} J/kg")

print("\nEntropies:")

print(f"S1 = {results['S'][0]:.2f} J/kg-K")

print(f"S2 = {results['S'][1]:.2f} J/kg-K")

print(f"S3 = {results['S'][2]:.2f} J/kg-K")

print(f"S4 = {results['S'][3]:.2f} J/kg-K")

print("\nCycle Performance:")

print(f"Refrigeration Effect = {results['Q_in']:.2f} J/kg")

print(f"Compressor Work      = {results['W_comp']:.2f} J/kg")

print(f"COP                  = {results['COP']:.2f}")

# ------------------------------------------------
# PLOT T-S DIAGRAM
# ------------------------------------------------

plot_refrigeration_ts(
    results["T"],
    results["S"],
    results["H"],
    results["P"]
)