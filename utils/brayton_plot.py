import matplotlib.pyplot as plt
import numpy as np
import math

def plot_ts_diagram(T1, T2, T3, T4, gamma):

    R = 8.314
    Cp = gamma * R / (gamma - 1)

    # -------------------------
    # State Entropies
    # -------------------------

    S1 = 0

    # 1 → 2 isentropic
    S2 = S1

    # 2 → 3 constant pressure heat addition
    delta_s_23 = Cp * math.log(T3 / T2)

    S3 = S2 + delta_s_23

    # 3 → 4 isentropic
    S4 = S3

    # -------------------------
    # Process 1 → 2
    # -------------------------

    T12 = np.linspace(T1, T2, 100)

    S12 = np.full(100, S1)

    # -------------------------
    # Process 2 → 3
    # -------------------------

    T23 = np.linspace(T2, T3, 100)

    S23 = Cp * np.log(T23 / T2)

    # -------------------------
    # Process 3 → 4
    # -------------------------

    T34 = np.linspace(T3, T4, 100)

    S34 = np.full(100, S3)

    # -------------------------
    # Process 4 → 1
    # -------------------------

    T41 = np.linspace(T4, T1, 100)

    S41 = S3 - Cp * np.log(T4 / T41)

    # -------------------------
    # Plotting
    # -------------------------

    plt.figure(figsize=(7,5))

    plt.plot(S12, T12, linewidth=2)

    plt.plot(S23, T23, linewidth=2)

    plt.plot(S34, T34, linewidth=2)

    plt.plot(S41, T41, linewidth=2)

    plt.xlabel("Entropy (J/K)")

    plt.ylabel("Temperature (K)")

    plt.title("Ideal Brayton Cycle T-S Diagram")

    plt.grid(True)

    plt.show()