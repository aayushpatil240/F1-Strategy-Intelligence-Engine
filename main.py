import json
from core.strategy import generate_strategies
from core.monte_carlo import run_monte_carlo_all
from analysis.comparison import rank_strategies, explain_strategy

def main():
    with open("data/sample_race.json", "r") as f:
        race_data = json.load(f)

    strategies = generate_strategies(race_data["total_laps"])

    print("Running Monte Carlo Simulation...\n")

    results = run_monte_carlo_all(strategies[:5], race_data, num_simulations=100)

    formatted = []
    for r in results:
        formatted.append({
            "strategy": r["strategy"],
            "total_time": r["avg_time"],
            "win_prob": r["win_prob"]
        })

    ranked = rank_strategies(formatted)

    print("\nTop Strategies (Monte Carlo):\n")

    for i, r in enumerate(ranked):
        explanation = explain_strategy(r["strategy"], race_data)

        print(f"{i+1}. {r['strategy']['type']}")
        print(f"   Avg Time: {r['total_time']:.2f} sec")
        print(f"   Win Probability: {r['win_prob']:.2f}%")
        print(f"   Delta: +{r['delta']:.2f}")
        print(f"   → {explanation}\n")


if __name__ == "__main__":
    main()