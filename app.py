import streamlit as st
from core.strategy import generate_strategies
from core.monte_carlo import run_monte_carlo_all
from analysis.comparison import rank_strategies
from visualization.plots import plot_strategy_timeline, plot_degradation
from analysis.comparison import generate_engineer_notes
from utils.ui import show_comparison_table
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# -------- TRON CSS --------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #020202, #000000);
    color: #e0e0e0;
}

/* Glass */
.block-container {
    background: rgba(255, 0, 0, 0.02);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 0, 0, 0.15);
}

/* 🔴 MAIN TITLE — TRUE TRON */
h1 {
    color: #ff0000 !important;
    font-weight: 900;
    letter-spacing: 2px;
    animation: flicker 2s infinite alternate;

    text-shadow:
        0 0 2px #ff0000,
        0 0 6px #ff0000,
        0 0 12px #ff0000,
        0 0 25px rgba(255,0,0,0.9),
        0 0 50px rgba(255,0,0,0.7),
        0 0 100px rgba(255,0,0,0.5);
}

/* Flicker Animation */
@keyframes flicker {
    0% { opacity: 1; }
    45% { opacity: 0.85; }
    60% { opacity: 0.6; }
    70% { opacity: 1; }
    85% { opacity: 0.9; }
    100% { opacity: 1; }
}

/* Subheaders */
h2, h3 {
    color: #ff1a1a !important;
    text-shadow:
        0 0 6px #ff0000,
        0 0 12px rgba(255,0,0,0.6);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(145deg, #000000, #080808);
    color: #ff0000;
    border: 1px solid #ff0000;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #ff0000;
    color: black;
    box-shadow:
        0 0 10px #ff0000,
        0 0 20px #ff0000,
        0 0 40px rgba(255,0,0,0.8);
}

/* Inputs */
input, select {
    background-color: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,0,0,0.3) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Slider glow */
.stSlider > div > div {
    color: #ff0000;
}

/* 🔥 Strategy Card */
.strategy-card {
    background: rgba(255,0,0,0.03);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,0,0,0.2);
    transition: all 0.3s ease;
}

.strategy-card:hover {
    transform: scale(1.01);
    box-shadow:
        0 0 10px #ff0000,
        0 0 20px rgba(255,0,0,0.6);
}

/* Pulsing glow */
@keyframes pulse {
    0% { box-shadow: 0 0 5px #ff0000; }
    50% { box-shadow: 0 0 20px #ff0000; }
    100% { box-shadow: 0 0 5px #ff0000; }
}

</style>
""", unsafe_allow_html=True)

# -------- TITLE --------
st.markdown("<h1> F1 Strategy Intelligence Engine</h1>", unsafe_allow_html=True)

# -------- TRACKS --------
TRACKS = {
    "Bahrain": {"laps": 57, "pit_loss": 20},
    "Monaco": {"laps": 78, "pit_loss": 25},
    "Silverstone": {"laps": 52, "pit_loss": 18},
    "Spa": {"laps": 44, "pit_loss": 21},
    "Monza": {"laps": 53, "pit_loss": 19},
    "Suzuka": {"laps": 53, "pit_loss": 20},
    "Singapore": {"laps": 62, "pit_loss": 23},
    "Abu Dhabi": {"laps": 58, "pit_loss": 21},
    "Austria": {"laps": 71, "pit_loss": 17},
    "Canada": {"laps": 70, "pit_loss": 19}
}

# -------- CONFIG --------
st.header("⚙️ Race Configuration")

c1, c2, c3 = st.columns(3)

with c1:
    selected_track = st.selectbox("Select Track", list(TRACKS.keys()))
with c2:
    sc_prob = st.slider("Safety Car Probability", 0.0, 1.0, 0.2)
with c3:
    sim_runs = st.slider("Monte Carlo Runs", 50, 500, 100)
    st.markdown("---")

st.subheader("🌦 Race Conditions")

c7, c8, c9 = st.columns(3)

with c7:
    weather = st.selectbox(
        "Weather",
        [
            "Dry",
            "Light Rain",
            "Heavy Rain",
            "Mixed Conditions"
        ]
    )

with c8:
    track_temp = st.slider(
        "Track Temperature (°C)",
        20,
        55,
        35
    )

with c9:
    fuel_load = st.slider(
        "Starting Fuel Load (kg)",
        80,
        110,
        100
    )

c10, c11, c12 = st.columns(3)

with c10:
    driver_aggression = st.slider(
        "Driver Aggression",
        1,
        10,
        5
    )

with c11:
    track_evolution = st.selectbox(
        "Track Evolution",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

with c12:
    traffic = st.selectbox(
        "Traffic Level",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

total_laps = TRACKS[selected_track]["laps"]
pit_loss = TRACKS[selected_track]["pit_loss"]

st.write(f"📍 Track: {selected_track}")
st.write(f"🏁 Laps: {total_laps} | ⏱ Pit Loss: {pit_loss}")

# -------- TYRES --------
st.subheader("🛞 Tyre Settings")

c4, c5, c6 = st.columns(3)

with c4:
    soft_base = st.slider("Soft Base Time", 85.0, 100.0, 90.0)
    soft_deg = st.slider("Soft Deg", 0.05, 0.3, 0.15)

with c5:
    med_base = st.slider("Medium Base Time", 85.0, 100.0, 91.0)
    med_deg = st.slider("Medium Deg", 0.05, 0.2, 0.10)

with c6:
    hard_base = st.slider("Hard Base Time", 85.0, 100.0, 92.0)
    hard_deg = st.slider("Hard Deg", 0.03, 0.15, 0.07)

race_data = {
    "track_name": selected_track,
    "total_laps": total_laps,
    "pit_loss_time": pit_loss,

    "weather": weather,
    "track_temperature": track_temp,
    "fuel_load": fuel_load,
    "driver_aggression": driver_aggression,
    "track_evolution": track_evolution,
    "traffic": traffic,

    "safety_car_probability": sc_prob,

    "tyres": {
        "soft": {
            "base_lap_time": soft_base,
            "deg_per_lap": soft_deg
        },
        "medium": {
            "base_lap_time": med_base,
            "deg_per_lap": med_deg
        },
        "hard": {
            "base_lap_time": hard_base,
            "deg_per_lap": hard_deg
        },
    },
}

# -------- RUN --------
# -------- RUN --------
st.markdown("---")

if st.button("🚀 Run Simulation"):

    strategies = generate_strategies(total_laps)

    results = run_monte_carlo_all(
        strategies[:5],
        race_data,
        num_simulations=sim_runs
    )

    formatted = [{
        "strategy": r["strategy"],
        "total_time": r["avg_time"],
        "win_prob": r["win_prob"]
    } for r in results]

    ranked = rank_strategies(formatted)

    # Strategy Comparison Table
    show_comparison_table(ranked)

    # Best Strategy
    best = ranked[0]
    engineer = generate_engineer_notes(
    best["strategy"],
    race_data
)

    st.header("🏆 Recommended Strategy")

    # -----------------------------
    # Basic Strategy Information
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🏎️ Strategy", best["strategy"]["type"].upper())
        st.metric("🏆 Strategy Score", f"{best['score']}/100")
        st.metric("⚠️ Risk", best["risk"])

    with col2:
        st.metric("🎯 Win Probability", f"{best['win_prob']:.1f}%")
        st.metric("📈 Confidence", best["confidence"])
        st.metric("⏱️ Expected Race Time", f"{best['total_time']:.2f}s")

    st.markdown("---")

    # =====================================================
    # ENGINEER DASHBOARD
    # =====================================================

    st.subheader("🧠 Engineer Dashboard")

    # =====================================================
    # STINT PLAN
    # =====================================================

    st.markdown("### 🏁 Stint Plan")

    engineer = generate_engineer_notes(best["strategy"], race_data)
    timeline_html = "<div style='display:flex; width:100%; height:50px; margin-bottom:30px;'>"

    total_laps = race_data["total_laps"]

    for stint in engineer["stints"]:

        start, end = stint["laps"].split("→")

        width = (
            (int(end.strip()) - int(start.strip()) + 1)
            / total_laps
        ) * 100

        tyre = stint["tyre"]

        if tyre == "Soft":
            color = "#ff3333"

        elif tyre == "Medium":
            color = "#ffd633"

        else:
            color = "#dddddd"

        timeline_html += (
            f"<div style='"
            f"width:{width}%;"
            f"background:{color};"
            f"color:black;"
            f"display:flex;"
            f"align-items:center;"
            f"justify-content:center;"
            f"font-weight:bold;"
            f"border-radius:8px;"
            f"margin-right:5px;"
            f"'>"
            f"{tyre}"
            f"</div>"
        )

    timeline_html += "</div>"

    st.markdown(timeline_html, unsafe_allow_html=True)

    for stint in engineer["stints"]:

        tyre = stint["tyre"]
        laps = stint["laps"]

        objective = stint["objective"]

        with st.container(border=True):

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Stint", stint["number"])

            with c2:
                st.metric("Tyre", tyre)

            with c3:
                st.metric("Laps", laps)

            st.write(f"**Objective:** {objective}")
            st.write(f"**Focus:** {stint['focus']}")

    st.markdown("---")

        # =====================================================
    # TYRE DEGRADATION GRAPH
    # =====================================================

    st.markdown("### 📈 Tyre Degradation")

    fig, ax = plt.subplots(figsize=(8, 3))

    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#050505")

    ax.tick_params(colors="white")

    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("#ff0000")

    for spine in ax.spines.values():
        spine.set_color("#ff0000")

    for stint in engineer["stints"]:

        tyre = stint["tyre"].lower()

        start, end = stint["laps"].split("→")

        laps = list(
            range(
                int(start.strip()),
                int(end.strip()) + 1
            )
        )

        degradation = []

        grip = 100

        for lap in laps:

            degradation.append(grip)

            grip -= race_data["tyres"][tyre]["deg_per_lap"] * 10

        ax.plot(
            laps,
            degradation,
            label=stint["tyre"]
        )

    ax.set_xlabel("Lap")
    ax.set_ylabel("Tyre Performance (%)")

    ax.set_title(
        "Tyre Life Simulation",
        fontsize=14,
        fontweight="bold"
    )

    legend = ax.legend()

    for text in legend.get_texts():
        text.set_color("white")

    legend.get_frame().set_facecolor("#111111")
    legend.get_frame().set_edgecolor("#ff0000")

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # LAP TIME GRAPH
    # =====================================================

    st.markdown("### 📉 Lap Time Evolution")

    fig2, ax2 = plt.subplots(figsize=(8, 3))

    fig2.patch.set_facecolor("#000000")
    ax2.set_facecolor("#050505")

    ax2.tick_params(colors="white")

    ax2.xaxis.label.set_color("white")
    ax2.yaxis.label.set_color("white")
    ax2.title.set_color("#ff0000")

    for spine in ax2.spines.values():
        spine.set_color("#ff0000")


    for stint in engineer["stints"]:

        tyre = stint["tyre"].lower()

        start, end = stint["laps"].split("→")

        laps = list(
            range(
                int(start.strip()),
                int(end.strip()) + 1
            )
        )

        lap_times = []

        base_time = race_data["tyres"][tyre]["base_lap_time"]

        for index, lap in enumerate(laps):

             tyre_loss = (
                (index ** 1.25)
                *
                race_data["tyres"][tyre]["deg_per_lap"]
            )

             fuel_gain = lap * 0.03

             lap_time = (
                base_time
                + tyre_loss
                - fuel_gain
            )

             lap_times.append(lap_time)
             lap_times.append(lap_time)


        ax2.plot(
            laps,
            lap_times,
            label=stint["tyre"]
        )


    ax2.set_xlabel("Lap")
    ax2.set_ylabel("Lap Time (sec)")

    ax2.set_title(
        "Race Pace Evolution",
        fontsize=14,
        fontweight="bold"
    )

    legend2 = ax2.legend()

    for text in legend2.get_texts():
        text.set_color("white")

    legend2.get_frame().set_facecolor("#111111")
    legend2.get_frame().set_edgecolor("#ff0000")

    st.pyplot(fig2)

    st.markdown("---")


    # =====================================================
    # PIT STRATEGY
    # =====================================================

    st.markdown("### ⛽ Pit Strategy")

    with st.container(border=True):

        if best["strategy"]["type"] == "1-stop":

            window = best["strategy"]["pit_window"]

            c1, c2 = st.columns(2)

            with c1:
                st.metric("Ideal Pit", best["strategy"]["ideal_pit"])

            with c2:
                st.metric(
                    "Pit Window",
                    f"{window[0]} - {window[2]}"
                )

        else:

            for i, window in enumerate(best["strategy"]["pit_window"]):

                st.write(
                    f"**Stop {i+1}:** "
                    f"{window[0]} - {window[2]} "
                    f"(Ideal {window[1]})"
                )

    st.markdown("---")

    # =====================================================
    # SAFETY CAR
    # =====================================================

    st.markdown("### 🚨 Safety Car")

    with st.container(border=True):

        sc = race_data["safety_car_probability"]

        if sc > 0.5:

            st.success(
                "High Safety Car probability.\n\n"
                "Pit immediately if it falls inside your pit window."
            )

        elif sc > 0.2:

            st.warning(
                "Moderate Safety Car probability.\n\n"
                "Stay flexible with pit timing."
            )

        else:

            st.info(
                "Low Safety Car probability.\n\n"
                "Commit to the planned strategy."
            )

    st.markdown("---")

    # =====================================================
    # ENGINEER NOTES
    # =====================================================

    st.markdown("### 🎯 Engineer Notes")

    with st.container(border=True):

        for note in engineer["notes"]:
         st.write(f"✅ {note}")
    