import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

def plot_refrigeration_ts(T, S, H, P):

    refrigerant = 'R134a'

    T1, T2, T3, T4 = T
    S1, S2, S3, S4 = S
    H1, H2, H3, H4 = H
    P_evap, P_cond = P

    # ------------------------------------------------
    # SATURATION DOME
    # ------------------------------------------------
    T_crit = 374.0
    T_sat = np.linspace(170, T_crit, 5000)
    s_liquid, s_vapor = [], []

    for temp in T_sat:
        try:
            s_liquid.append(PropsSI('S', 'T', temp, 'Q', 0, refrigerant))
            s_vapor.append(PropsSI('S', 'T', temp, 'Q', 1, refrigerant))
        except:
            s_liquid.append(np.nan)
            s_vapor.append(np.nan)

    s_crit = PropsSI('S', 'T', T_crit, 'Q', 0, refrigerant)

    plt.figure(figsize=(10, 6))

    # ------------------------------------------------
    # PROCESS 1 → 2 (Compressor — straight line)
    # ------------------------------------------------
    plt.plot([S1, S2], [T1, T2],
             linewidth=2, color='blue', label='Compression')

    # ------------------------------------------------
    # PROCESS 2 → 3 (Condenser)
    # Sweep H from H2 to H3 at constant P_cond
    # ------------------------------------------------
    T23, S23 = [], []

    for h in np.linspace(H2, H3, 400):
        try:
            T23.append(PropsSI('T', 'P', P_cond, 'H', h, refrigerant))
            S23.append(PropsSI('S', 'P', P_cond, 'H', h, refrigerant))
        except:
            T23.append(np.nan)
            S23.append(np.nan)

    # Force exact connection to state 2 and state 3
    T23[0] = T2
    S23[0] = S2
    T23[-1] = T3
    S23[-1] = S3

    plt.plot(S23, T23, linewidth=2, color='orange', label='Condensation')

    # ------------------------------------------------
    # PROCESS 3 → 4 (Expansion Valve — straight line)
    # ------------------------------------------------
    plt.plot([S3, S4], [T3, T4],
             linewidth=2, color='green', label='Expansion Valve')

    # ------------------------------------------------
    # PROCESS 4 → 1 (Evaporator — sweep H at constant P_evap)
    # ------------------------------------------------
    T41, S41 = [], []

    for h in np.linspace(H4, H1, 300):
        try:
            T41.append(PropsSI('T', 'P', P_evap, 'H', h, refrigerant))
            S41.append(PropsSI('S', 'P', P_evap, 'H', h, refrigerant))
        except:
            T41.append(np.nan)
            S41.append(np.nan)

    plt.plot(S41, T41, linewidth=2, color='red', label='Evaporation')

    # ------------------------------------------------
    # SATURATION DOME — plotted on top
    # ------------------------------------------------
    # After the dome loop, before plotting:
    s_liquid_arr = np.array(s_liquid)
    s_vapor_arr = np.array(s_vapor)

    # Replace last point of both with exact critical entropy to force closure
    s_liquid_arr[-1] = s_crit
    s_vapor_arr[-1] = s_crit

    plt.plot(s_liquid_arr, T_sat, color='black', linewidth=1.5, zorder=5)
    plt.plot(s_vapor_arr,  T_sat, color='black', linewidth=1.5, zorder=5)
    plt.plot(s_crit, T_crit, 'ko', markersize=4, zorder=6)

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------
    plt.scatter([S1, S2, S3, S4], [T1, T2, T3, T4],
                color='red', s=60, zorder=10)

    for s, t, lbl in zip([S1, S2, S3, S4], [T1, T2, T3, T4],
                          ['1', '2', '3', '4']):
        plt.text(s + 5, t + 1, lbl, fontsize=12,
                 fontweight='bold', zorder=11)

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------
    plt.xlabel('Entropy (J/kg-K)')
    plt.ylabel('Temperature (K)')
    plt.title('Vapor Compression Refrigeration Cycle T-S Diagram')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()