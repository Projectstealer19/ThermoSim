import matplotlib.pyplot as plt

def plot_ts_diagram( Th , Tc , delta_s):

    S1 = 5 #reference entropy state
    S2 = S1 + delta_s

    entropy = [S1 , S2 , S2 , S1 , S1]
    temperature = [600, 600, 300, 300, 600]

    plt.plot(entropy, temperature, marker='o')

    plt.xlabel("Entropy (J/K)")
    plt.ylabel("Temperature (K)")
    plt.title("Carnot Cycle T-S Diagram")

    plt.grid(True)

    plt.show()