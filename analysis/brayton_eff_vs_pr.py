import matplotlib.pyplot as plt
import numpy as np

def plot_efficiency_vs_rp():
    gamma = 1.4
    rp_values = np.linspace(2, 20, 100)
    exponent = (gamma - 1) / gamma
    efficiencies = (1 - (1 / (rp_values ** exponent))) * 100

    plt.figure(figsize=(7,5))
    plt.plot(rp_values, efficiencies, linewidth=2, color='#4a9edd')
    plt.xlabel("Pressure Ratio (rp)")
    plt.ylabel("Thermal Efficiency (%)")
    plt.title("Brayton Cycle Efficiency vs Pressure Ratio")
    plt.grid(True)
    plt.tight_layout()
    plt.show()