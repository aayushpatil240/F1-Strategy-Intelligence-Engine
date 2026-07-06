def generate_strategies(total_laps):
    """
    Generate 1-stop and 2-stop race strategies.

    Each strategy now contains:
    - Strategy type
    - Stints
    - Tyre sequence
    - Pit laps
    - Ideal pit lap(s)
    - Recommended pit window(s)
    """

    strategies = []

    # -----------------------------
    # 1-STOP STRATEGIES
    # -----------------------------
    for pit_lap in range(10, total_laps - 10, 5):

        strategy = {
            "type": "1-stop",

            "stints": [
                {"start": 1, "end": pit_lap},
                {"start": pit_lap + 1, "end": total_laps}
            ],

            # New fields
            "tyres": ["Soft", "Medium"],

            "pit_laps": [pit_lap],

            "ideal_pit": pit_lap,

            "pit_window": [
                max(1, pit_lap - 2),
                pit_lap,
                min(total_laps, pit_lap + 2)
            ]
        }

        strategies.append(strategy)

    # -----------------------------
    # 2-STOP STRATEGIES
    # -----------------------------
    for pit1 in range(10, total_laps - 20, 10):

        for pit2 in range(pit1 + 10, total_laps - 10, 10):

            strategy = {

                "type": "2-stop",

                "stints": [
                    {"start": 1, "end": pit1},
                    {"start": pit1 + 1, "end": pit2},
                    {"start": pit2 + 1, "end": total_laps}
                ],

                "tyres": [
                    "Soft",
                    "Medium",
                    "Hard"
                ],

                "pit_laps": [
                    pit1,
                    pit2
                ],

                "ideal_pit": [
                    pit1,
                    pit2
                ],

                "pit_window": [
                    [
                        max(1, pit1 - 2),
                        pit1,
                        min(total_laps, pit1 + 2)
                    ],
                    [
                        max(1, pit2 - 2),
                        pit2,
                        min(total_laps, pit2 + 2)
                    ]
                ]
            }

            strategies.append(strategy)

    return strategies