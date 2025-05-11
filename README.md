# Typing Blast

Typing Blast is an arcade-style typing shooter game built with Python and Pygame. Players must defend their ship by typing words that appear as enemies. The faster and more accurately you type, the longer you survive and the higher your score.

---

## Game Concept

You pilot a spaceship in a scrolling starfield. Enemies in the form of **words** slowly descend toward your base. To destroy them, you must **type each word correctly**. Every correctly typed letter fires a bullet. The game becomes progressively harder as waves increase, challenging both your typing speed and precision.
---

## Screenshots

### Gameplay Preview

<div align="center">
  <img src="screenshot/gameplay/1.png" width="400"/>
  <img src="screenshot/gameplay/2.png" width="400"/>
  <img src="screenshot/gameplay/3.png" width="400"/>
  <img src="screenshot/gameplay/4.png" width="400"/>
</div>

### Data Visualization Dashboard

<div align="center">
  <img src="screenshot/visualization/1.png" width="400"/>
  <img src="screenshot/visualization/2.png" width="400"/>
  <img src="screenshot/visualization/3.png" width="400"/>
  <img src="screenshot/visualization/4.png" width="400"/>
  <img src="screenshot/visualization/5.png" width="400"/>
  <img src="screenshot/visualization/6.png" width="400"/>
  <img src="screenshot/visualization/7.png" width="400"/>
  <img src="screenshot/visualization/8.png" width="400"/>
  <img src="screenshot/visualization/9.png" width="400"/>
  <img src="screenshot/visualization/10.png" width="400"/>
</div>

**Features:**

* Real-time word-based enemy system
* Combo tracking, score, accuracy, and words-per-minute (WPM) tracking
* Sound effects for typing and errors
* Visual stats dashboard and game-over summary
* Dynamic difficulty scaling with wave-based spawning

---

## Game Strategy

* Focus on the leftmost letters first—correct keystrokes destroy words one character at a time.
* Try to maintain high accuracy to maximize score multipliers and combo bonuses.
* The words move faster as you progress through waves. Prioritize words nearing your base.
* Avoid typing incorrect letters, as errors reduce your combo and score.

---

## Project Architecture (MVC Pattern)

Typing Blast follows the **Model-View-Controller (MVC)** architecture for maintainability and scalability.

### Controller (Game Logic)

* **`state_controller.py`** – Manages transitions between game states (menu, playing, game over, stats).
* **`game_controller.py`** – Core logic of the game loop, collision detection, wave progression, word spawning.

### Views (Rendering/UI)

* **`menu.py`** – Animated menu screen with starfield and buttons.
* **`game_view.py`** – Renders the game scene, including wave animations and stats.
* **`dashboard_view.py`** – Displays real-time stats like WPM, accuracy, score.
* **`stats_view.py`** – Shows visual charts using matplotlib of performance over time.
* **`gameover_view.py`** – Displays final stats and lets player return to the menu.
* **`wave_view.py`** – Briefly displays the wave number on screen with fade-out animation.

### Models (Game Data & Entities)

* **`word.py`** – Represents each word enemy; handles movement, state, and destruction.
* **`letter.py`** – Individual letter sprite tied to each word.
* **`rocket.py`** – Player's ship graphic.
* **`bullet.py`** – Bullets fired on correct keystrokes.

---

## Project Structure

```plaintext
TypingBlast/
├── main.py                  # App entry point
├── Models/
│   ├── word.py              # Word entity
│   ├── letter.py            # Letter sprite
│   ├── rocket.py            # Player sprite
│   ├── bullet.py            # Projectile sprite
├── Views/
│   ├── menu.py              # Main menu screen
│   ├── game_view.py         # Gameplay rendering
│   ├── gameover_view.py     # Game over screen
│   ├── stats_view.py        # Statistics with charts
│   ├── dashboard_view.py    # Real-time game stats
│   ├── wave_view.py         # Wave transition animation
├── Controllers/
│   ├── state_controller.py  # State switching logic
│   ├── game_controller.py   # Game progression, input handling
├── Utils/
│   ├── config.py            # CLI argument parser
│   ├── settings.py          # Game constants
│   ├── sound_manager.py     # Handles all game sounds
│   ├── layout.py            # Layout alignment utilities
│   ├── screen.py            # Screen setup and drawing
│   ├── clock.py             # Framerate control
│   ├── randomizer.py        # Safe spawning random logic
│   ├── save_to_csv.py       # Session stat logger
│   ├── wordspawner.py       # Prevent overlapping word spawn
├── assets/
│   ├── images/              # rocket.png, bullet.png
│   ├── sounds/              # typing.wav, error.wav, game_over.wav
├── results.csv              # Game stats saved after each run
└── README.md                # This file
```
---

### UML Class Diagram

![UML Class Diagram](./uml.png)

---

## Statistics & Performance Tracking

After each game:

* Stats (WPM, Accuracy, Combo, Score) are saved to `results.csv`.
* The **Stats View** reads this file and shows graphs (WPM trend, accuracy trend, etc.).
* Useful for tracking typing performance over time!


### Performance Analytics: Descriptive Statistics & Data Visualization

The **Typing Blast Stats Dashboard** is an advanced analytical tool built with `CustomTkinter`, `Pandas`, and `Matplotlib` to help players understand and improve their typing performance. After each gameplay session, player statistics are recorded into `results.csv` and automatically visualized through an interactive GUI.

### Descriptive Statistics

Inside the **Descriptive Stats** tab, players can:

* **Select any numeric column** (e.g., WPM, Accuracy, Score) for detailed analysis
* View well-organized statistical summaries, grouped into:

  * **Centrality**

    * Count, Mean, Median, Mode
  * **Dispersion**

    * Min, Max, Range, Variance, Standard Deviation, Coefficient of Variation (CV), Mean Absolute Deviation (MAD), Quartiles (Q1, Q3), and Interquartile Range (IQR)
  * **Outlier Detection**

    * Both IQR-based (Q1–1.5*IQR, Q3+1.5*IQR) and SD-based (Mean ± 3\*SD) methods
* Results are presented in expandable, neatly styled panels with automatic layout and scroll support.

### Visualization Tab

The **Visualization** tab supports dynamic plotting using Matplotlib embedded in the Tkinter interface. Users can choose from:

* **Scatter Plot:** Visualize relationships between any two numeric variables (e.g., WPM vs Accuracy)
* **Histogram:** View distribution and frequency of selected metrics
* **Line Chart:** Track performance trends across sessions
* **Boxplot:** Analyze spread, median, and outliers for a variable

Each chart is generated on-demand, and users can switch variables directly through dropdowns.

### Comparison Tab

The **Comparison** tab allows:

* Selection of **two variables** to visualize and compare side-by-side in a line graph
* Insights into correlation and performance progression across metrics

This feature is perfect for evaluating how improvements in one aspect (e.g., accuracy) affect another (e.g., score).

### Raw Data Viewer

Finally, the **Raw Data** tab provides a table-like view using `ttk.Treeview`, offering:

* Full visibility of every recorded session
* Scrollable and sortable interface for reviewing past game results
* Useful for exporting or analyzing in external tools
---
## Requirements
To run this project, install the dependencies below:

```
pygame>=2.1.0
customtkinter>=5.2.2
matplotlib>=3.5.0
pandas>=1.3.0
numpy>=1.21.0
```

Install them via pip:

```bash
pip install -r requirements.txt
```

---

## How to Play

1. Run `main.py` to launch the game.
2. Use your keyboard to type the falling words.
3. Monitor stats live or open the dashboard separately to analyze past results.


---

## Future Improvements

* Power-ups (slow motion, bomb, etc.)
* Leaderboard system with user profiles
---
