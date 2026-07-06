import streamlit as st


def show_comparison_table(ranked):
    """
    Display the strategy comparison table.
    """

    st.header("📊 Strategy Comparison")

    comparison_data = []

    for i, strategy in enumerate(ranked):

        comparison_data.append({

            "Rank": f"#{i+1}",

            "Strategy": strategy["strategy"]["type"],

            "Score": strategy["score"],

            "Win %": f"{strategy['win_prob']:.1f}%",

            "Risk": strategy["risk"],

            "Confidence": strategy["confidence"],

            "Pit Stops": strategy["pit_stops"],

            "Race Time": f"{strategy['total_time']:.2f}s",

            "Delta": f"+{strategy['delta']:.2f}s"

        })

    st.dataframe(
    comparison_data,
    width="stretch",
    hide_index=True
)

    st.markdown("---")