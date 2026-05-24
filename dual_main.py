from cycles.dual import dual_cycle

from utils.dual_plot import (
    plot_dual_pv,
    plot_dual_ts
)

# ------------------------------------------------
# USER INPUTS
# ------------------------------------------------

T1 = float(input("Enter initial temperature T1 (K): "))

r = float(input("Enter compression ratio r: "))

alpha = float(input("Enter pressure ratio alpha (P3/P2): "))

rc = float(input("Enter cut-off ratio rc (V4/V3): "))

gamma = float(input("Enter gamma (Cp/Cv): "))

# ------------------------------------------------
# RUN DUAL CYCLE
# ------------------------------------------------

results = dual_cycle(T1, r, alpha, rc, gamma)

# ------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------

print("\n===== Dual Cycle Results =====")

print(f"\nT1 = {results['T'][0]:.2f} K")

print(f"T2 = {results['T'][1]:.2f} K")

print(f"T3 = {results['T'][2]:.2f} K")

print(f"T4 = {results['T'][3]:.2f} K")

print(f"T5 = {results['T'][4]:.2f} K")

print(f"\nHeat Added     = {results['Q_in']:.2f} J/kg")

print(f"Heat Rejected  = {results['Q_out']:.2f} J/kg")

print(f"Net Work       = {results['W_net']:.2f} J/kg")

print(f"Efficiency     = {results['efficiency']:.2f}%")

# ------------------------------------------------
# STATE POINTS
# ------------------------------------------------

print("\nState Points:")

for i in range(5):

    print(
        f"  State {i+1}: "
        f"V = {results['V'][i]:.6f} m³  |  "
        f"P = {results['P'][i]:.2f} Pa"
    )

# ------------------------------------------------
# PLOTS
# ------------------------------------------------

plot_dual_pv(results)

plot_dual_ts(results)