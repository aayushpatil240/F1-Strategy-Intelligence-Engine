import random
from copy import deepcopy
from core.simulation import simulate_strategy


def run_monte_carlo_all(strategies, race_data, num_simulations=100):
    """
    Run Monte Carlo across all strategies.
    """

    results = []

    for strat in strategies:
        results.append({
            "strategy": strat,
            "times": [],
            "wins": 0
        })

    for _ in range(num_simulations):

        # Deep copy so original race_data never changes
        modified_data = deepcopy(race_data)

        # -------------------------------------------------
        # Random tyre degradation variation
        # -------------------------------------------------

        for tyre in modified_data["tyres"]:

            base_deg = modified_data["tyres"][tyre]["deg_per_lap"]

            variation = random.uniform(-0.02, 0.02)

            modified_data["tyres"][tyre]["deg_per_lap"] = max(
                0.01,
                base_deg + variation
            )

        # -------------------------------------------------
        # WEATHER
        # -------------------------------------------------

        weather = modified_data["weather"]

        if weather == "Light Rain":

            modified_data["pit_loss_time"] *= 1.03

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] += 2

        elif weather == "Heavy Rain":

            modified_data["pit_loss_time"] *= 1.08

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] += 5

        elif weather == "Mixed Conditions":

            modified_data["pit_loss_time"] *= 1.02

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] += random.uniform(1, 4)

        # -------------------------------------------------
        # TRACK TEMPERATURE
        # -------------------------------------------------

        temp = modified_data["track_temperature"]

        if temp > 40:

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["deg_per_lap"] *= 1.15

        elif temp < 25:

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["deg_per_lap"] *= 0.90

        # -------------------------------------------------
        # FUEL LOAD
        # -------------------------------------------------

        fuel = modified_data["fuel_load"]

        fuel_factor = (fuel - 80) * 0.015

        for tyre in modified_data["tyres"]:
            modified_data["tyres"][tyre]["base_lap_time"] += fuel_factor

        # -------------------------------------------------
        # DRIVER AGGRESSION
        # -------------------------------------------------

        aggression = modified_data["driver_aggression"]

        pace_gain = aggression * 0.08
        wear_gain = aggression * 0.03

        for tyre in modified_data["tyres"]:

            modified_data["tyres"][tyre]["base_lap_time"] -= pace_gain

            modified_data["tyres"][tyre]["deg_per_lap"] += wear_gain

        # -------------------------------------------------
        # TRACK EVOLUTION
        # -------------------------------------------------

        evolution = modified_data["track_evolution"]

        if evolution == "High":

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] -= 0.40

        elif evolution == "Medium":

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] -= 0.20

        # -------------------------------------------------
        # TRAFFIC
        # -------------------------------------------------

        traffic = modified_data["traffic"]

        if traffic == "Medium":

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] += 0.30

        elif traffic == "High":

            for tyre in modified_data["tyres"]:
                modified_data["tyres"][tyre]["base_lap_time"] += 0.80

        # -------------------------------------------------
        # SAFETY CAR
        # -------------------------------------------------

        if random.random() < modified_data["safety_car_probability"]:
            modified_data["pit_loss_time"] *= 0.70

        # -------------------------------------------------
        # Simulate
        # -------------------------------------------------

        times = []

        for r in results:

            t = simulate_strategy(
                r["strategy"],
                modified_data
            )

            r["times"].append(t)

            times.append(t)

        winner = min(times)

        for r in results:

            if r["times"][-1] == winner:

                r["wins"] += 1

    # -------------------------------------------------
    # Final Statistics
    # -------------------------------------------------

    for r in results:

        r["avg_time"] = sum(r["times"]) / len(r["times"])

        r["win_prob"] = (r["wins"] / num_simulations) * 100

    return results