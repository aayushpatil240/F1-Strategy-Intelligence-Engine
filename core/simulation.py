from core.tyre_model import get_lap_time

def simulate_strategy(strategy, race_data):
    """
    Simulate total race time for a given strategy.

    Returns:
    - total_time (float)
    """

    tyres = race_data["tyres"]
    pit_loss = race_data["pit_loss_time"]

    total_time = 0

    # For simplicity: assign tyre compounds per stint
    tyre_sequence = ["soft", "medium", "hard"]

    for stint_index, stint in enumerate(strategy["stints"]):
        tyre_type = tyre_sequence[stint_index % len(tyre_sequence)]
        tyre_data = tyres[tyre_type]

        stint_laps = stint["end"] - stint["start"] + 1

        for lap in range(1, stint_laps + 1):
            lap_time = get_lap_time(tyre_data, lap)
            total_time += lap_time

        # Add pit stop (except after last stint)
        if stint_index < len(strategy["stints"]) - 1:
            total_time += pit_loss

    return total_time