import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

def plot_rankine_ts(T, S, H, P_boiler, P_cond):

    T1, T2, T3, T4 = T
    S1, S2, S3, S4 = S
    h1, h2, h3, h4 = H

    # ------------------------------------------------
    # SATURATION DOME
    # ------------------------------------------------
    T_sat = np.linspace(273.16, 647.095, 2000)
    s_liquid, s_vapor = [], []

    for temp in T_sat:
        try:
            s_liquid.append(PropsSI('S', 'T', temp, 'Q', 0, 'Water'))
            s_vapor.append(PropsSI('S', 'T', temp, 'Q', 1, 'Water'))
        except:
            s_liquid.append(np.nan)
            s_vapor.append(np.nan)

    T_crit = 647.095
    s_crit = PropsSI('S', 'T', T_crit, 'Q', 0, 'Water')

    plt.figure(figsize=(10, 6))

    # ------------------------------------------------
    # PROCESS 1 → 2 (Pump — straight line, crosses pressures)
    # ------------------------------------------------
    plt.plot([S1, S2], [T1, T2], linewidth=2, color='blue', label='Pump')

    # ------------------------------------------------
    # PROCESS 2 → 3 (Boiler — real path at constant P_boiler)
    # ------------------------------------------------
    T_sat_boiler = PropsSI('T', 'P', P_boiler, 'Q', 1, 'Water')
    h_sat_vapor  = PropsSI('H', 'P', P_boiler, 'Q', 1, 'Water')

    T23, S23 = [], []

    # Subcooled + two-phase
    for h in np.linspace(h2, h_sat_vapor, 250):
        try:
            T23.append(PropsSI('T', 'P', P_boiler, 'H', h, 'Water'))
            S23.append(PropsSI('S', 'P', P_boiler, 'H', h, 'Water'))
        except:
            T23.append(np.nan)
            S23.append(np.nan)

    # Superheating
    for temp in np.linspace(T_sat_boiler, T3, 201)[1:]:
        try:
            T23.append(temp)
            S23.append(PropsSI('S', 'P', P_boiler, 'T', temp, 'Water'))
        except:
            T23.append(np.nan)
            S23.append(np.nan)

    plt.plot(S23, T23, linewidth=2, color='orange', label='Boiler')

    # ------------------------------------------------
    # PROCESS 3 → 4 (Non-Ideal Turbine — straight line)
    # Irreversible expansion: pressure crosses P_boiler → P_cond
    # No single pressure applies to intermediate points,
    # so straight line from state 3 to state 4 is correct
    # ------------------------------------------------
    plt.plot([S3, S4], [T3, T4], linewidth=2, color='green', label='Turbine')

    # ------------------------------------------------
    # PROCESS 4 → 1 (Condenser — horizontal line at T_cond)
    # Isothermal two-phase condensation at P_cond
    # ------------------------------------------------
    plt.plot([S4, S1], [T1, T1], linewidth=2, color='red', label='Condenser')

    # ------------------------------------------------
    # SATURATION DOME
    # ------------------------------------------------
    plt.plot(s_liquid, T_sat, color='black', linewidth=1.5, zorder=5)
    plt.plot(s_vapor,  T_sat, color='black', linewidth=1.5, zorder=5)
    plt.plot(s_crit, T_crit, 'ko', markersize=5, zorder=6)

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------
    plt.scatter([S1, S2, S3, S4], [T1, T2, T3, T4],
                color='red', s=50, zorder=10)

    for s, t, label in zip([S1, S2, S3, S4], [T1, T2, T3, T4],
                            ['1', '2', '3', '4']):
        plt.text(s, t, label, fontsize=12, fontweight='bold',
                 verticalalignment='bottom', zorder=11)

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------
    plt.xlabel('Entropy (J/kg-K)')
    plt.ylabel('Temperature (K)')
    plt.title('Non-Ideal Rankine Cycle T-S Diagram')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()