# console-based

# Graphical Games & Calculator Suite

A clean, zero-dependency collection of five lightweight graphical desktop applications built using the Python Standard Library (`tkinter`).

---

## Repository Modules

* **`snake.py`:** Classic arcade game using vector queues and coordinate collision verification.
* **`sudoku.py`:** Interactive puzzle board featuring live input filters and automatic grid checking.
* **`tic_tac_toe.py`:** Two-player grid layout matching real-time input selections to win-vector matrices.
* **`minesweeper.py`:** Grid-clearing minefield game with right-click flagging and recursive empty-cell cascades.
* **`calculator.py`:** Modern math calculator handling real-time evaluations with explicit zero-division overrides.

---

## Setup & Execution

### Prerequisites
* Operating System: Windows, macOS, or Linux.
* Environment: **Python 3.8+** (No third-party packages required).

### Run an Application
Open your terminal inside the project directory and run any chosen module file node directly:

```bash
# Launch Snake
python3 snake.py

# Launch Sudoku
python3 sudoku.py

# Launch Tic-Tac-Toe
python3 tic_tac_toe.py

# Launch Minesweeper
python3 minesweeper.py

# Launch Calculator
python3 calculator.py


## Architectural Highlights
# ​Encapsulation: Every application operates within its own decoupled, object-oriented class structure.
# ​Input Safety: Interactive inputs are sanitized using strict string filters (isdigit()) to ensure absolute execution stability.
