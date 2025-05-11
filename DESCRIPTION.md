## **Typing Blast: Project Description**

### Overview

**Typing Blast** is a fast-paced, wave-based typing shooter game designed to sharpen typing skills and hand-eye coordination. Players must destroy falling words by typing them accurately and quickly. As the game progresses through waves, difficulty increases with faster word speeds and more complex vocabulary. It’s not just a game — it's a test of reflex, focus, and accuracy.

The game is implemented in Python using the Pygame library, following the **MVC (Model-View-Controller)** architecture. Additionally, it includes a dedicated **Stats Dashboard** built with **CustomTkinter**, which visualizes player performance over multiple sessions using graphs and tables.

---

### Concept

* Players control a **rocket** at the bottom of the screen.
* Words fall from the top, and players must **type the words correctly** to destroy them.
* Every successful keystroke fires a **bullet** toward the word.
* The game progresses in **waves**; each wave increases word speed and complexity.
* Mistakes reduce accuracy and score.
* Game ends when too many words reach the bottom or the player fails to maintain performance.

---

### Key Features

* **Rocket & Bullet mechanics**: Auto-fire bullets on correct keystrokes.
* **Real-time word tracking**: Each letter must be typed in sequence.
* **Wave System**: Difficulty increases over 12 waves.
* **Sound effects**: Typing, errors, wave transitions, and game over.
* **Game Over View**: Shows WPM, accuracy, score, errors, and wave reached.
* **Stats Dashboard**:

  * Descriptive statistics like WPM, Accuracy, Score, Errors.
  * Session-by-session line graphs for performance tracking.
  * Matplotlib-powered visualizations embedded in a modern CustomTkinter GUI.

---

### UML Class Diagram

> Embed this on TPM using the following HTML tag:
```html
<img src="https://github.com/sklv1ain/TypingBlast/raw/main/uml.png" alt="UML Class Diagram">
```

You can find the full source code and documentation in the [TypingBlast GitHub Repository](https://github.com/SKlv1ain/TypingBlast).