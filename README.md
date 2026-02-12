# ⚡ Terminal Typing Test

A sleek, lightweight, and cross-platform **Typing Speed Test** built entirely in Python. No heavy libraries like `curses` required—just pure ANSI magic for a smooth terminal experience.

---

## ✨ Features

* **🚀 Real-time Stats:** Track your **WPM** (Words Per Minute), **CPM** (Characters Per Minute), and **Accuracy** as you type.
* **👻 Ghost Words:** Preview upcoming words to maintain your typing flow.
* **🎨 Visual Feedback:** Instant color-coding (Green for correct, Red for mistakes).
* **💻 Cross-Platform:** Works seamlessly on **Windows, macOS, and Linux**.
* **📦 Zero Dependencies:** Uses standard Python libraries and ANSI escape codes.

---

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/terminal-typing-test.git](https://github.com/yourusername/terminal-typing-test.git)
    cd terminal-typing-test
    ```

2.  **Run the game:**
    ```bash
    python typing_test.py
    ```

---

## 🎮 How to Play

* **Start:** Press `ENTER` to reveal the words and begin typing to start the 60-second timer.
* **Submit Word:** Press `SPACE` to move to the next word.
* **Correcting:** Use `BACKSPACE` to fix errors in your current word.
* **Quit:** Press `ESC` at any time to exit the game.

---

## 📊 Performance Ratings

Can you reach the top tier?

| WPM | Rating |
| :--- | :--- |
| **60+** | 🔥 Excellent! |
| **40 - 60** | 👍 Good! |
| **20 - 40** | 📝 Keep Practicing! |
| **< 20** | 💪 Room for Improvement! |

---

## 🛠️ Technical Details

This project demonstrates:
* **Low-level Input Handling:** Using `msvcrt` for Windows and `termios/tty` for Unix-based systems to capture keystrokes without requiring the user to press Enter.
* **Multithreading:** A background thread manages the countdown timer for precise updates.
* **ANSI Escape Sequences:** Custom cursor positioning (`\033[s`, `\033[u`) and color formatting for a dynamic UI within a standard terminal buffer.

---

## 📜 License

This project is open-source and available under the **MIT License**.
