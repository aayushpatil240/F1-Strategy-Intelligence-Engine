def get_lap_time(tyre_data, lap_number):
    """
    Calculate lap time based on tyre degradation.

    Parameters:
    - tyre_data: dict (base_lap_time, deg_per_lap)
    - lap_number: int (lap in the stint)

    Returns:
    - lap_time: float
    """

    base_time = tyre_data["base_lap_time"]
    degradation = tyre_data["deg_per_lap"]

    lap_time = base_time + (lap_number * degradation)

    return lap_time