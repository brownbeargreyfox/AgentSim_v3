import matplotlib.pyplot as plt

def plot_override_trends(data):
    plt.plot(data)
    plt.title("Override Frequency Over Time")
    plt.xlabel("Turns")
    plt.ylabel("Overrides")
    plt.show()
