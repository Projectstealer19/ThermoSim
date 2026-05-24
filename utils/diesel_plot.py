import matplotlib.pyplot as plt
import numpy as np

def plot_diesel_ts(T, S):

    T1, T2, T3, T4 = T

    S1, S2, S3, S4 = S

    plt.figure(figsize=(9, 6))

    # ------------------------------------------------
    # PROCESS 1 → 2
    # Isentropic Compression
    # ------------------------------------------------

    T12 = np.linspace(T1, T2, 200)

    S12 = np.full_like(T12, S1)

    plt.plot(
        S12,
        T12,
        linewidth=2,
        color='blue',
        label='Compression'
    )

    # ------------------------------------------------
    # PROCESS 2 → 3
    # Constant Pressure Heat Addition
    # ------------------------------------------------

    T23 = np.linspace(T2, T3, 200)

    S23 = np.linspace(S2, S3, 200)

    plt.plot(
        S23,
        T23,
        linewidth=2,
        color='orange',
        label='Heat Addition'
    )

    # ------------------------------------------------
    # PROCESS 3 → 4
    # Isentropic Expansion
    # ------------------------------------------------

    T34 = np.linspace(T3, T4, 200)

    S34 = np.full_like(T34, S3)

    plt.plot(
        S34,
        T34,
        linewidth=2,
        color='green',
        label='Expansion'
    )

    # ------------------------------------------------
    # PROCESS 4 → 1
    # Constant Volume Heat Rejection
    # ------------------------------------------------

    T41 = np.linspace(T4, T1, 200)

    S41 = np.linspace(S4, S1, 200)

    plt.plot(
        S41,
        T41,
        linewidth=2,
        color='red',
        label='Heat Rejection'
    )

    # ------------------------------------------------
    # STATE POINTS
    # ------------------------------------------------

    plt.scatter(
        [S1, S2, S3, S4],
        [T1, T2, T3, T4],
        color='black',
        s=50,
        zorder=5
    )

    for s, t, label in zip(
        [S1, S2, S3, S4],
        [T1, T2, T3, T4],
        ['1', '2', '3', '4']
    ):

        plt.text(
            s,
            t,
            label,
            fontsize=12,
            fontweight='bold'
        )

    # ------------------------------------------------
    # GRAPH SETTINGS
    # ------------------------------------------------

    plt.xlabel('Entropy (J/kg-K)')

    plt.ylabel('Temperature (K)')

    plt.title('Ideal Diesel Cycle T-S Diagram')

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()