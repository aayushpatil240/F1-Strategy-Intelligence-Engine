# F1 Strategy Intelligence Engine

## Introduction

F1 Strategy Intelligence Engine is a race strategy simulation and analysis tool designed to model Formula 1 race decision-making.

The project simulates different race strategies by considering tyre behaviour, pit stop timing, race conditions, safety car probability, and performance changes over a race distance. It uses Monte Carlo simulations to test multiple possible race scenarios and recommends the most effective strategy based on performance, risk, and consistency.

The goal of this project is to recreate the type of decision-support system used by race strategists to evaluate strategy options before and during a race.

---

## Tech Stack

- **Python**
  - Core programming language used for race simulation, strategy logic, and data processing.

- **Streamlit**
  - Used to create an interactive web dashboard for configuring race scenarios and displaying strategy results.

- **Monte Carlo Simulation**
  - Used to simulate multiple race outcomes by introducing randomness in tyre degradation, safety car events, and race conditions.

- **Matplotlib**
  - Used for visualizing tyre degradation trends and lap time evolution.

- **Custom Strategy Engine**
  - Generates and evaluates different race strategies including one-stop and two-stop approaches.

- **Data Processing & Analysis**
  - Calculates strategy scores, risk levels, confidence values, and performance comparisons.

---

# Working

The system follows a race engineering workflow:

## 1. Race Configuration

The user selects race parameters such as:

- Circuit
- Number of Monte Carlo simulations
- Safety car probability
- Weather conditions
- Track temperature
- Fuel load
- Driver aggression level
- Track evolution
- Traffic conditions

These inputs define the expected race environment.

---

## 2. Strategy Generation

The strategy engine automatically generates possible race plans.

Examples:

- One-stop strategy  
  Soft → Medium

- Two-stop strategy  
  Soft → Medium → Hard

Each strategy contains:

- Tyre compounds
- Stint lengths
- Pit stop windows
- Ideal pit laps

---

## 3. Monte Carlo Simulation

Instead of testing each strategy only once, the system runs multiple race simulations.

During every simulation, variables such as:

- Tyre degradation variation
- Safety car occurrence
- Pit stop advantage
- Race uncertainty

are randomly adjusted.

This allows the engine to understand how each strategy performs under changing race conditions.

---

## 4. Strategy Ranking Algorithm

After simulations are completed, each strategy is evaluated based on:

- Average race time
- Win probability
- Number of pit stops
- Risk level
- Strategy flexibility

A final strategy score is calculated and the strongest option is recommended.

---

## 5. Engineer Analysis Dashboard

The recommended strategy is converted into a race engineering report containing:

- Stint-by-stint plan
- Tyre management advice
- Pit window analysis
- Safety car strategy
- Fuel and traffic considerations
- Race condition insights

The dashboard provides information similar to what engineers analyze when preparing race strategy decisions.

---

# Features

- Interactive Formula 1 race strategy simulator

- Monte Carlo based strategy prediction

- Automatic one-stop and two-stop strategy generation

- Strategy comparison and ranking system

- Dynamic race condition inputs

- Safety car probability modeling

- Weather and track condition analysis

- Tyre degradation simulation

- Lap time evolution visualization

- Visual stint timeline

- Pit window recommendations

- Strategy confidence and risk evaluation

- Engineer-style race analysis dashboard

---

# Use Case

This project demonstrates how simulation and data analysis can support decision-making in motorsport.

Possible applications include:

- Motorsport race strategy analysis
- Race simulation tools
- Performance engineering studies
- Data-driven decision systems
- Understanding Formula 1 strategy planning

It combines software engineering, simulation techniques, and motorsport analytics to create an interactive strategy intelligence system.

---

# Screenshots
<img width="1912" height="928" alt="f1 strat 1" src="https://github.com/user-attachments/assets/2d48e96b-112b-45f0-88bc-88fc9edb0259" />
<img width="1917" height="850" alt="f1 strat 2" src="https://github.com/user-attachments/assets/75929f64-f3ce-4c93-9c41-b3de4d369fcb" />
<img width="1901" height="668" alt="f1 strat 3" src="https://github.com/user-attachments/assets/da29bb5f-6861-410a-b983-e025b5cb35da" />
<img width="1919" height="911" alt="f1 strat 4" src="https://github.com/user-attachments/assets/dffb4710-1362-4275-89ca-813dabf28040" />
<img width="1918" height="916" alt="f1 strat 5" src="https://github.com/user-attachments/assets/184e995b-d3a0-4ca3-b8a4-eac4c164186c" />
<img width="1896" height="886" alt="f1 strat 6" src="https://github.com/user-attachments/assets/b95c505f-d982-4ac3-aecc-1785d285f952" />


