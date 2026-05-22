import matplotlib.pyplot as plt
import numpy as np

def plot_efficiency_vs_rp(gamma):

    rp_values = np.linspace(2, 20, 100)

    efficiencies = []

    exponent = (gamma - 1) / gamma

    for rp in rp_values:

        eta = 1 - (1 / (rp ** exponent))

        efficiencies.append(eta * 100)

    # Plot

    plt.figure(figsize=(7,5))

    plt.plot(rp_values, efficiencies, linewidth=2)

    plt.xlabel("Pressure Ratio (rp)")

    plt.ylabel("Thermal Efficiency (%)")

    plt.title("Brayton Cycle Efficiency vs Pressure Ratio")

    plt.grid(True)

    plt.show()