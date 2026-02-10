# Game of Life

A simple Python implementation of Conway’s Game of Life, playable in the terminal with interactive controls.

---

## Features

- Random initial board generation  
- Classic Game of Life rules  
- Interactive controls: pause/resume and quit  
- Clean terminal display at each generation  

---

## Requirements

- Python 3  
- [`keyboard`](https://pypi.org/project/keyboard/) library installed in your virtual environment:

```bash
pip install keyboard
```

Running the Game

Activate your virtual environment, then run:

```bash
sudo $(which python3) game_of_life.py
```

Using sudo with the Python from your venv lets the game detect keyboard input without installing the library system-wide.

## Controls

    SPACE → Pause / Resume

    Q → Quit the game cleanly

The terminal is cleared at each generation so the board updates in place. Exiting leaves the terminal clean.

## Optional Parameters

You can adjust the board size and speed by modifying the run_life parameters in game_of_life.py:

```python
run_life(board_width=80, board_height=40, interval_s=0.1)
```
