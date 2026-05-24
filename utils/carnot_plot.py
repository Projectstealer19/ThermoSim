import matplotlib.pyplot as plt
import numpy as np

def plot_pv_diagram(results):

    V1, V2, V3, V4 = results["V"]
    P1, P2, P3, P4 = results["P"]
    Th    = results["Th"]
    Tc    = results["Tc"]
    nR    = results["nR"]
    gamma = results["gamma"]

    # ------------------------------------------------
    # PROCESS 1 → 2 (Isothermal expansion at Th)
    # ------------------------------------------------
    V12 = np.linspace(V1, V2, 300)
    P12 = nR * Th / V12

    # ------------------------------------------------
    # PROCESS 2 → 3 (Adiabatic expansion)
    # ------------------------------------------------
    V23 = np.linspace(V2, V3, 300)
    P23 = P2 * (V2 / V23) ** gamma

    # ------------------------------------------------
    # PROCESS 3 → 4 (Isothermal compression at Tc)
    # ------------------------------------------------
    V34 = np.linspace(V3, V4, 300)
    P34 = nR * Tc / V34

    # ------------------------------------------------
    # PROCESS 4 → 1 (Adiabatic compression)
    # ------------------------------------------------
    V41 = np.linspace(V4, V1, 300)
    P41 = P4 * (V4 / V41) ** gamma

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------
    plt.figure(figsize=(9, 6))

    plt.plot(V12, P12, color='red',    linewidth=2, label='1→2 Isothermal Expansion (Th)')
    plt.plot(V23, P23, color='blue',   linewidth=2, label='2→3 Adiabatic Expansion')
    plt.plot(V34, P34, color='orange', linewidth=2, label='3→4 Isothermal Compression (Tc)')
    plt.plot(V41, P41, color='green',  linewidth=2, label='4→1 Adiabatic Compression')

    # State points
    V_pts = [V1, V2, V3, V4]
    P_pts = [P1, P2, P3, P4]
    plt.scatter(V_pts, P_pts, color='black', s=60, zorder=5)

    for i, (v, p) in enumerate(zip(V_pts, P_pts)):
        plt.text(v, p, f' {i+1}', fontsize=12, fontweight='bold', zorder=6)

    plt.xlabel('Volume (m³)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Carnot Cycle P-V Diagram')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------
# T-S DIAGRAM FUNCTION
# ------------------------------------------------

def plot_ts_diagram(results):

    S1, S2, S3, S4 = results["S"]

    Th, _, Tc, _ = results["T"]

    # ------------------------------------------------
    # PROCESS 1 → 2
    # Isothermal Expansion at Th
    # ------------------------------------------------

    S12 = np.linspace(S1, S2, 300)

    T12 = np.full_like(S12, Th)

    # ------------------------------------------------
    # PROCESS 2 → 3
    # Adiabatic Expansion
    # ------------------------------------------------

    S23 = np.full(300, S2)

    T23 = np.linspace(Th, Tc, 300)

    # ------------------------------------------------
    # PROCESS 3 → 4
    # Isothermal Compression at Tc
    # ------------------------------------------------

    S34 = np.linspace(S3, S4, 300)

    T34 = np.full_like(S34, Tc)

    # ------------------------------------------------
    # PROCESS 4 → 1
    # Adiabatic Compression
    # ------------------------------------------------

    S41 = np.full(300, S1)

    T41 = np.linspace(Tc, Th, 300)

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------

    plt.figure(figsize=(9, 6))

    plt.plot(
        S12,
        T12,
        color='red',
        linewidth=2,
        label='1→2 Isothermal Expansion (Th)'
    )

    plt.plot(
        S23,
        T23,
        color='blue',
        linewidth=2,
        label='2→3 Adiabatic Expansion'
    )

    plt.plot(
        S34,
        T34,
        color='orange',
        linewidth=2,
        label='3→4 Isothermal Compression (Tc)'
    )

    plt.plot(
        S41,
        T41,
        color='green',
        linewidth=2,
        label='4→1 Adiabatic Compression'
    )

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------

    S_pts = [S1, S2, S3, S4]

    T_pts = [Th, Th, Tc, Tc]

    plt.scatter(
        S_pts,
        T_pts,
        color='black',
        s=60,
        zorder=5
    )

    for i, (s, t) in enumerate(zip(S_pts, T_pts)):

        plt.text(
            s,
            t,
            f' {i+1}',
            fontsize=12,
            fontweight='bold',
            zorder=6
        )

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------

    plt.xlabel('Entropy (J/K)')

    plt.ylabel('Temperature (K)')

    plt.title('Carnot Cycle T-S Diagram')

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()