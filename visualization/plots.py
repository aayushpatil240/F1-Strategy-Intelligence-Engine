import matplotlib.pyplot as plt

def plot_strategy_timeline(strategy, total_laps):
    fig, ax = plt.subplots()

    for stint in strategy["stints"]:
        ax.barh(
            y=1,
            width=stint["end"] - stint["start"],
            left=stint["start"],
        )

    ax.set_xlabel("Lap")
    ax.set_title("Strategy Timeline")
    ax.set_yticks([])

    return fig


def plot_degradation(tyre_data, laps=30):
    times = []
    for lap in range(1, laps + 1):
        time = tyre_data["base_lap_time"] + lap * tyre_data["deg_per_lap"]
        times.append(time)

    fig, ax = plt.subplots()
    ax.plot(range(1, laps + 1), times)
    ax.set_title("Tyre Degradation Curve")
    ax.set_xlabel("Lap")
    ax.set_ylabel("Lap Time")

    return fig