import matplotlib.pyplot as plt
import numpy as np

def plot_diesel_pv(results):

    V1, V2, V3, V4 = results["V"]
    P1, P2, P3, P4 = results["P"]
    gamma = results["gamma"]

    # ------------------------------------------------
    # PROCESS 1 → 2 (Isentropic compression)
    # ------------------------------------------------
    V12 = np.linspace(V1, V2, 300)
    P12 = P1 * (V1 / V12) ** gamma

    # ------------------------------------------------
    # PROCESS 2 → 3 (Constant pressure heat addition)
    # ------------------------------------------------
    V23 = np.linspace(V2, V3, 300)
    P23 = np.full(300, P2)

    # ------------------------------------------------
    # PROCESS 3 → 4 (Isentropic expansion)
    # ------------------------------------------------
    V34 = np.linspace(V3, V4, 300)
    P34 = P3 * (V3 / V34) ** gamma

    # ------------------------------------------------
    # PROCESS 4 → 1 (Constant volume heat rejection)
    # ------------------------------------------------
    V41 = np.full(300, V1)
    P41 = np.linspace(P4, P1, 300)

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------
    plt.figure(figsize=(9, 6))

    plt.plot(V12, P12, color='blue',   linewidth=2, label='1→2 Isentropic Compression')
    plt.plot(V23, P23, color='orange', linewidth=2, label='2→3 Constant Pressure Heat Addition')
    plt.plot(V34, P34, color='green',  linewidth=2, label='3→4 Isentropic Expansion')
    plt.plot(V41, P41, color='red',    linewidth=2, label='4→1 Constant Volume Heat Rejection')

    # State points
    V_pts = [V1, V2, V3, V4]
    P_pts = [P1, P2, P3, P4]
    plt.scatter(V_pts, P_pts, color='black', s=60, zorder=5)

    for i, (v, p) in enumerate(zip(V_pts, P_pts)):
        plt.text(v, p, f' {i+1}', fontsize=12, fontweight='bold', zorder=6)

    plt.xlabel('Volume (m³)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Ideal Diesel Cycle P-V Diagram')
    plt.grid(True)
    plt.legend()
    plt.figtext(0.12, 0.01,
                "Assumptions: Ideal gas, V1=0.001 m³, P1=101325 Pa (atmospheric)",
                fontsize=8, color='gray')
    plt.tight_layout()
    plt.show()

# ------------------------------------------------
# T-S DIAGRAM FUNCTION
# ------------------------------------------------

def plot_diesel_ts(results):

    import matplotlib.pyplot as plt
    import numpy as np

    S1, S2, S3, S4 = results["S"]

    T1, T2, T3, T4 = results["T"]

    cp = results["cp"]

    cv = results["cv"]

    # ------------------------------------------------
    # PROCESS 1 → 2
    # Isentropic Compression
    # ------------------------------------------------

    S12 = np.full(300, S1)

    T12 = np.linspace(T1, T2, 300)

    # ------------------------------------------------
    # PROCESS 2 → 3
    # Constant Pressure Heat Addition
    # TRUE CURVED RELATION
    # ------------------------------------------------

    T23 = np.linspace(T2, T3, 300)

    S23 = S2 + cp * np.log(T23 / T2)

    # ------------------------------------------------
    # PROCESS 3 → 4
    # Isentropic Expansion
    # ------------------------------------------------

    S34 = np.full(300, S3)

    T34 = np.linspace(T3, T4, 300)

    # ------------------------------------------------
    # PROCESS 4 → 1
    # Constant Volume Heat Rejection
    # TRUE CURVED RELATION
    # ------------------------------------------------

    T41 = np.linspace(T4, T1, 300)

    S41 = S4 + cv * np.log(T41 / T4)

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------

    plt.figure(figsize=(9, 6))

    plt.plot(
        S12,
        T12,
        color='blue',
        linewidth=2,
        label='1→2 Isentropic Compression'
    )

    plt.plot(
        S23,
        T23,
        color='orange',
        linewidth=2,
        label='2→3 Constant Pressure Heat Addition'
    )

    plt.plot(
        S34,
        T34,
        color='green',
        linewidth=2,
        label='3→4 Isentropic Expansion'
    )

    plt.plot(
        S41,
        T41,
        color='red',
        linewidth=2,
        label='4→1 Constant Volume Heat Rejection'
    )

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------

    S_pts = [S1, S2, S3, S4]

    T_pts = [T1, T2, T3, T4]

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

    plt.xlabel('Entropy (J/kg-K)')

    plt.ylabel('Temperature (K)')

    plt.title('Ideal Diesel Cycle T-S Diagram')

    plt.grid(True)

    plt.legend()

    plt.figtext(
        0.12,
        0.01,
        "Assumptions: Ideal gas, reference entropy baseline used",
        fontsize=8,
        color='gray'
    )

    plt.tight_layout()

    plt.show()    