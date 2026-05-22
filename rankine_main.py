from cycles.rankine import rankine_cycle

from utils.rankine_plot import plot_rankine_ts

# -------------------------
# User Inputs
# -------------------------

P_boiler = float(input("Enter Boiler Pressure (Pa): "))

P_cond = float(input("Enter Condenser Pressure (Pa): "))

T3 = float(input("Enter Turbine Inlet Temperature T3 (K): "))

eta_turbine = float(input("Enter Turbine Efficiency (0-1): "))

eta_pump = float(input("Enter Pump Efficiency (0-1): "))

# -------------------------
# Run Rankine Cycle
# -------------------------

results = rankine_cycle(
    P_boiler,
    P_cond,
    T3,
    eta_turbine,
    eta_pump
)

# -------------------------
# Display Results
# -------------------------

print("\n===== Rankine Cycle Results =====")

print("\nTemperatures:")

for i, temp in enumerate(results["T"], start=1):

    print(f"T{i} = {temp:.2f} K")

print("\nEntropies:")

for i, entropy in enumerate(results["S"], start=1):

    print(f"S{i} = {entropy:.2f} J/kg-K")

print("\nEnthalpies:")

for i, enthalpy in enumerate(results["H"], start=1):

    print(f"H{i} = {enthalpy:.2f} J/kg")

print("\nCycle Performance:")

print(f"Turbine Work = {results['W_turbine']:.2f} J/kg")

print(f"Pump Work    = {results['W_pump']:.2f} J/kg")

print(f"Heat Added   = {results['Q_in']:.2f} J/kg")

print(f"Efficiency   = {results['efficiency']:.2f}%")

# -------------------------
# Plot T-S Diagram
# -------------------------

plot_rankine_ts(
    results["T"],
    results["S"],
    results["H"],
    P_boiler,
    P_cond
)