import matplotlib.pyplot as plt
import numpy as np

# =================================================
# P-V DIAGRAM
# =================================================

def plot_dual_pv(results):

    V1, V2, V3, V4, V5 = results["V"]

    P1, P2, P3, P4, P5 = results["P"]

    gamma = results["gamma"]

    # ------------------------------------------------
    # PROCESS 1 → 2
    # Isentropic Compression
    # ------------------------------------------------

    V12 = np.linspace(V1, V2, 300)

    P12 = P1 * (V1 / V12) ** gamma

    # ------------------------------------------------
    # PROCESS 2 → 3
    # Constant Volume Heat Addition
    # ------------------------------------------------

    V23 = np.full(300, V2)

    P23 = np.linspace(P2, P3, 300)

    # ------------------------------------------------
    # PROCESS 3 → 4
    # Constant Pressure Heat Addition
    # ------------------------------------------------

    V34 = np.linspace(V3, V4, 300)

    P34 = np.full(300, P3)

    # ------------------------------------------------
    # PROCESS 4 → 5
    # Isentropic Expansion
    # ------------------------------------------------

    V45 = np.linspace(V4, V5, 300)

    P45 = P4 * (V4 / V45) ** gamma

    # ------------------------------------------------
    # PROCESS 5 → 1
    # Constant Volume Heat Rejection
    # ------------------------------------------------

    V51 = np.full(300, V1)

    P51 = np.linspace(P5, P1, 300)

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        V12,
        P12,
        color='blue',
        linewidth=2,
        label='1→2 Isentropic Compression'
    )

    plt.plot(
        V23,
        P23,
        color='orange',
        linewidth=2,
        label='2→3 Constant Volume Heat Addition'
    )

    plt.plot(
        V34,
        P34,
        color='purple',
        linewidth=2,
        label='3→4 Constant Pressure Heat Addition'
    )

    plt.plot(
        V45,
        P45,
        color='green',
        linewidth=2,
        label='4→5 Isentropic Expansion'
    )

    plt.plot(
        V51,
        P51,
        color='red',
        linewidth=2,
        label='5→1 Constant Volume Heat Rejection'
    )

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------

    V_pts = [V1, V2, V3, V4, V5]

    P_pts = [P1, P2, P3, P4, P5]

    plt.scatter(
        V_pts,
        P_pts,
        color='black',
        s=60,
        zorder=5
    )

    for i, (v, p) in enumerate(zip(V_pts, P_pts)):

        plt.text(
            v,
            p,
            f' {i+1}',
            fontsize=12,
            fontweight='bold'
        )

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------

    plt.xlabel("Volume (m³)")

    plt.ylabel("Pressure (Pa)")

    plt.title("Ideal Dual Cycle P-V Diagram")

    plt.grid(True)

    plt.legend()

    plt.figtext(
        0.12,
        0.01,
        "Assumptions: Ideal gas, V1=0.001 m³, P1=101325 Pa",
        fontsize=8,
        color='gray'
    )

    plt.tight_layout()

    plt.show()


# =================================================
# T-S DIAGRAM
# =================================================

def plot_dual_ts(results):

    S1, S2, S3, S4, S5 = results["S"]

    T1, T2, T3, T4, T5 = results["T"]

    cv = results["cv"]

    cp = results["cp"]

    # ------------------------------------------------
    # PROCESS 1 → 2
    # Isentropic Compression
    # ------------------------------------------------

    S12 = np.full(300, S1)

    T12 = np.linspace(T1, T2, 300)

    # ------------------------------------------------
    # PROCESS 2 → 3
    # Constant Volume Heat Addition
    # ------------------------------------------------

    T23 = np.linspace(T2, T3, 300)

    S23 = S2 + cv * np.log(T23 / T2)

    # ------------------------------------------------
    # PROCESS 3 → 4
    # Constant Pressure Heat Addition
    # ------------------------------------------------

    T34 = np.linspace(T3, T4, 300)

    S34 = S3 + cp * np.log(T34 / T3)

    # ------------------------------------------------
    # PROCESS 4 → 5
    # Isentropic Expansion
    # ------------------------------------------------

    S45 = np.full(300, S4)

    T45 = np.linspace(T4, T5, 300)

    # ------------------------------------------------
    # PROCESS 5 → 1
    # Constant Volume Heat Rejection
    # ------------------------------------------------

    T51 = np.linspace(T5, T1, 300)

    S51 = S5 + cv * np.log(T51 / T5)

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------

    plt.figure(figsize=(10, 6))

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
        label='2→3 Constant Volume Heat Addition'
    )

    plt.plot(
        S34,
        T34,
        color='purple',
        linewidth=2,
        label='3→4 Constant Pressure Heat Addition'
    )

    plt.plot(
        S45,
        T45,
        color='green',
        linewidth=2,
        label='4→5 Isentropic Expansion'
    )

    plt.plot(
        S51,
        T51,
        color='red',
        linewidth=2,
        label='5→1 Constant Volume Heat Rejection'
    )

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------

    S_pts = [S1, S2, S3, S4, S5]

    T_pts = [T1, T2, T3, T4, T5]

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
            fontweight='bold'
        )

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------

    plt.xlabel("Entropy (J/kg-K)")

    plt.ylabel("Temperature (K)")

    plt.title("Ideal Dual Cycle T-S Diagram")

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