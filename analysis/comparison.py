def rank_strategies(results):
    """
    Rank strategies and calculate useful engineering metrics.
    """

    ranked = sorted(results, key=lambda x: x["total_time"])

    best_time = ranked[0]["total_time"]

    for r in ranked:

        # Delta
        r["delta"] = round(r["total_time"] - best_time, 2)

        # Number of pit stops
        stops = len(r["strategy"]["stints"]) - 1
        r["pit_stops"] = stops

        # Risk
        if stops == 1:
            r["risk"] = "Low"
        elif stops == 2:
            r["risk"] = "Medium"
        else:
            r["risk"] = "High"

        # Confidence
        if r["win_prob"] >= 70:
            r["confidence"] = "High"
        elif r["win_prob"] >= 40:
            r["confidence"] = "Medium"
        else:
            r["confidence"] = "Low"

        # Strategy Score
        score = 100

        score -= r["delta"] * 2
        score -= stops * 4

        if r["risk"] == "Medium":
            score -= 3

        if r["risk"] == "High":
            score -= 8

        r["score"] = max(0, min(100, round(score)))

        # Recommendation reasons
        reasons = []

        if r["delta"] < 2:
            reasons.append("Lowest expected race time")

        if r["win_prob"] > 50:
            reasons.append("Highest Monte Carlo success rate")

        if r["risk"] == "Low":
            reasons.append("Lowest strategy risk")

        if stops == 1:
            reasons.append("Minimal pit lane time loss")

        if not reasons:
            reasons.append("Alternative strategy if race conditions change")

        r["reasons"] = reasons

    return ranked


# ---------------------------------------------------------
# NEW
# ---------------------------------------------------------

def generate_strategy_brief(strategy, race_data):

    """
    Generate a detailed race engineer briefing.
    """

    stints = strategy["stints"]
    tyres = strategy["tyres"]

    sc = race_data["safety_car_probability"]
    total_laps = race_data["total_laps"]

    text = ""

    text += "=" * 65 + "\n"
    text += "                RACE ENGINEER STRATEGY BRIEF\n"
    text += "=" * 65 + "\n\n"

    text += f"Track: {race_data['track_name']}\n"
    text += f"Race Distance: {total_laps} Laps\n"
    text += f"Selected Strategy: {strategy['type'].upper()}\n"
    text += f"Safety Car Probability: {int(sc*100)}%\n\n"

    # =====================================================
    # STINT PLAN
    # =====================================================

    text += "-" * 65 + "\n"
    text += "1. STINT EXECUTION PLAN\n"
    text += "-" * 65 + "\n"

    for i, stint in enumerate(stints):

        tyre = tyres[i]

        start = stint["start"]
        end = stint["end"]
        length = end - start + 1

        text += f"\nStint {i+1}\n"
        text += f"Tyre Compound : {tyre}\n"
        text += f"Laps          : {start} → {end}\n"
        text += f"Length        : {length} laps\n"

        if tyre.lower() == "soft":
            text += (
                "Objective     : Attack aggressively while grip is highest.\n"
                "Focus         : Gain track position and build a gap.\n"
            )

        elif tyre.lower() == "medium":
            text += (
                "Objective     : Maintain consistent pace.\n"
                "Focus         : Control degradation and tyre temperatures.\n"
            )

        else:
            text += (
                "Objective     : Maximise tyre life.\n"
                "Focus         : Bring the car home with stable pace.\n"
            )

    text += "\n"

    # =====================================================
    # PIT WINDOWS
    # =====================================================

    text += "-" * 65 + "\n"
    text += "2. PIT STRATEGY\n"
    text += "-" * 65 + "\n"

    if strategy["type"] == "1-stop":

        window = strategy["pit_window"]

        text += (
            f"\nIdeal Pit Lap      : {strategy['ideal_pit']}\n"
            f"Recommended Window : {window[0]} → {window[2]}\n"
            "Reason             : Maximise tyre performance while avoiding excessive degradation.\n"
        )

    else:

        for i, window in enumerate(strategy["pit_window"]):

            text += (
                f"\nPit Stop {i+1}\n"
                f"Ideal Lap : {window[1]}\n"
                f"Window    : {window[0]} → {window[2]}\n"
            )

    text += "\n"

    # =====================================================
    # SAFETY CAR
    # =====================================================

    text += "-" * 65 + "\n"
    text += "3. SAFETY CAR DECISION\n"
    text += "-" * 65 + "\n"

    if sc >= 0.5:

        text += (
            "\nHIGH probability.\n\n"
            "- Pit immediately if Safety Car appears inside the pit window.\n"
            "- Extend first stint slightly if tyres remain healthy.\n"
            "- Prioritise track position over tyre freshness.\n"
        )

    elif sc >= 0.2:

        text += (
            "\nMEDIUM probability.\n\n"
            "- Stay flexible.\n"
            "- Box if Safety Car saves significant pit-loss time.\n"
            "- Avoid committing too early.\n"
        )

    else:

        text += (
            "\nLOW probability.\n\n"
            "- Follow the planned pit window.\n"
            "- Do not delay the stop waiting for a Safety Car.\n"
        )

    text += "\n"

    # =====================================================
    # TYRE MANAGEMENT
    # =====================================================

    text += "-" * 65 + "\n"
    text += "4. TYRE MANAGEMENT\n"
    text += "-" * 65 + "\n"

    text += (
        "\n• Minimise wheelspin on corner exits.\n"
        "• Avoid locking the front tyres under braking.\n"
        "• Monitor degradation every 5 laps.\n"
        "• Lift-and-coast if degradation rises above prediction.\n"
    )

    text += "\n"

    # =====================================================
    # OVERTAKING
    # =====================================================

    text += "-" * 65 + "\n"
    text += "5. RACE EXECUTION\n"
    text += "-" * 65 + "\n"

    text += (
        "\n• Push hardest during the first 3 laps after every pit stop.\n"
        "• Use tyre advantage for undercut opportunities.\n"
        "• Defend only against direct rivals to preserve tyres.\n"
        "• Avoid unnecessary battles early in the race.\n"
    )

    text += "\n"

    # =====================================================
    # FINAL STINT
    # =====================================================

    final = stints[-1]

    text += "-" * 65 + "\n"
    text += "6. FINAL STINT\n"
    text += "-" * 65 + "\n"

    text += (
        f"\nFinal Stint : Laps {final['start']} → {final['end']}\n"
        "Maintain tyre life until approximately 10 laps remain.\n"
        "Deploy maximum pace in the closing laps.\n"
    )

    text += "\n"

    # =====================================================
    # EXPECTED RESULT
    # =====================================================

    text += "-" * 65 + "\n"
    text += "7. EXPECTED OUTCOME\n"
    text += "-" * 65 + "\n"

    if strategy["type"] == "1-stop":

        text += (
            "\n✔ Low-risk strategy.\n"
            "✔ Strong overall race pace.\n"
            "✔ Best suited for races with limited interruptions.\n"
        )

    else:

        text += (
            "\n✔ Higher peak pace.\n"
            "✔ Better recovery after traffic.\n"
            "✔ Requires perfect pit execution.\n"
        )

    text += "\n"

    text += "=" * 65 + "\n"
    text += "END OF RACE ENGINEER BRIEF\n"
    text += "=" * 65

    return text
def generate_engineer_notes(strategy, race_data):
    """
    Returns structured engineer information for the dashboard.
    """

    stints = []

    for i, stint in enumerate(strategy["stints"]):

        tyre = strategy["tyres"][i]

        if tyre == "Soft":
            objective = "Attack aggressively while grip is highest."
            focus = "Build track position before tyre drop-off."

        elif tyre == "Medium":
            objective = "Maintain consistent race pace."
            focus = "Manage degradation and tyre temperatures."

        else:
            objective = "Bring the car safely to the finish."
            focus = "Avoid excessive wheelspin."

        stints.append({

            "number": i + 1,
            "tyre": tyre,
            "laps": f"{stint['start']} → {stint['end']}",
            "objective": objective,
            "focus": focus

        })

    # -----------------------------
    # Pit Strategy
    # -----------------------------

    if strategy["type"] == "1-stop":

        pit = {

            "ideal": strategy["ideal_pit"],
            "window": strategy["pit_window"],
            "reason": "Pit before tyre degradation becomes significant."

        }

    else:

        pit = {

            "ideal": None,
            "window": strategy["pit_window"],
            "reason": "Two-stop strategy maximises tyre performance."

        }

    # -----------------------------
    # Safety Car
    # -----------------------------

    sc = race_data["safety_car_probability"]

    if sc > 0.5:

        safety = {
            "level": "High",
            "advice": "Pit immediately if Safety Car falls inside the pit window."
        }

    elif sc > 0.2:

        safety = {
            "level": "Medium",
            "advice": "Stay flexible and prepare for an opportunistic stop."
        }

    else:

        safety = {
            "level": "Low",
            "advice": "Commit to the planned strategy."
        }

    

       # -----------------------------
    # Engineer Notes
    # -----------------------------

    notes = []

    # Weather Analysis
    if race_data["weather"] != "Dry":

        notes.append(
            f"🌦 Weather Analysis:\n"
            f"{race_data['weather']} conditions introduce strategy uncertainty. "
            "Monitor grip levels closely and be prepared to adjust the pit window "
            "if track conditions change."
        )

    else:

        notes.append(
            "🌦 Weather Analysis:\n"
            "Dry conditions allow a more predictable strategy. "
            "Focus on tyre degradation, pace consistency, and pit timing."
        )


    # Fuel Analysis
    if race_data["fuel_load"] > 105:

        notes.append(
            "⛽ Fuel Management:\n"
            "Heavy fuel load will reduce early race performance. "
            "Prioritize tyre conservation during the opening phase. "
            "Expect improved pace as fuel burns off."
        )

    else:

        notes.append(
            "⛽ Fuel Management:\n"
            "Lower fuel load allows stronger early pace. "
            "The driver can attack earlier without heavily compromising tyre life."
        )


    # Driver Aggression Analysis
    if race_data["driver_aggression"] >= 8:

        notes.append(
            "🛞 Tyre Management:\n"
            "Aggressive driving increases tyre stress and degradation. "
            "Manage traction zones carefully to avoid losing performance "
            "before the pit window."
        )

    elif race_data["driver_aggression"] <= 3:

        notes.append(
            "🛞 Tyre Management:\n"
            "Conservative driving style should extend tyre life. "
            "Longer stint flexibility is possible if race conditions change."
        )

    else:

        notes.append(
            "🛞 Tyre Management:\n"
            "Balanced driving approach provides a good compromise between "
            "lap time performance and tyre preservation."
        )


    # Track Evolution
    if race_data["track_evolution"] == "High":

        notes.append(
            "📈 Track Evolution:\n"
            "Track grip is expected to improve significantly. "
            "Later stints may become faster, increasing the value of extending tyre life."
        )

    else:

        notes.append(
            "📈 Track Evolution:\n"
            "Limited track improvement expected. Strategy performance will rely mainly "
            "on tyre management and clean execution."
        )


    # Traffic Analysis
    if race_data["traffic"] == "High":

        notes.append(
            "🚗 Traffic Strategy:\n"
            "High traffic risk around the pit window. "
            "Undercut opportunities should be considered to avoid losing time behind slower cars."
        )

    else:

        notes.append(
            "🚗 Traffic Strategy:\n"
            "Traffic risk is manageable. The strategy can prioritize optimal tyre performance "
            "rather than reacting to other cars."
        )


    # Pit Window Insight
    notes.append(
        "⛽ Pit Window Assessment:\n"
        "The recommended pit window balances tyre degradation, track position, "
        "and potential race interruptions."
    )
    
    return {
        "stints": stints,
        "pit": pit,
        "safety": safety,
        "notes": notes
    }