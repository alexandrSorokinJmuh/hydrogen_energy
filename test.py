import matplotlib.pyplot as plt
import numpy as np

labels = ['Siege', 'Initiation', 'Crowd_control', 'Wave_clear', 'Objective_damage', 'asd', 'dddd']


def make_radar_chart(name, stats, attribute_labels=labels, plot_markers=[0, 0.2, 0.4, 0.6, 0.8, 1], plot_str_markers=["0", "0.2", "0.4", "0.6", "0.8", "1"]):
    labels = np.array(attribute_labels)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    plt.yticks(plot_markers)
    ax.set_title(name)
    ax.grid(True)

    fig.savefig("%s.png" % name)

    return plt.show()


make_radar_chart("Agni", [0.2, 0.7, 0.5, 0.15, 0.9, 0.3, 1])  # example
