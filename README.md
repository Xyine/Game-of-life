# Game of Life
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern and extensible implementation of Conway’s Game of Life in Python, featuring both a graphical interface and a powerful command-line mode.

Built as a clean, modular, and developer-friendly simulation engine.

## Features

- Graphical interface (pygame)

- Interactive terminal mode

- Multiple rule sets (Classic, Zombie, Von Neumann, Respawn)

- Load predefined patterns (Blinker, Pulsar, LWSS)

- Zoom & scroll support (GUI)

- Clean architecture (engine / GUI / CLI separation)

- Fast setup using uv

## Quick Start

Windows users:

This project targets a Unix-like environment.

On Windows, please use WSL2.


Clone the repository:

```bash
git clone https://github.com/xyine/game-of-life.git
cd game-of-life
```


Install (dev mode):

This project uses uv for fast Python environments.

```bash
make install-dev
```

This will:

Create a virtual environment

Install dependencies

Install the project in editable mode

## Run the Game

GUI Mode:

```bash
make game
```

Terminal Mode use the CLI:

```bash
sudo $(which python3) main.py terminal
```

You can use argument to 
Examples:
```bash
sudo $(which python3) main.py terminal --width 40 --height 40
sudo $(which python3) main.py terminal --file board_file/pulsar.json
sudo $(which python3) main.py terminal --interval 0.1
```

## Controls

GUI:

Mouse wheel → Zoom

Arrow keys → Move camera

Settings panel → Rules, speed, patterns

Terminal:

Key	Action
SPACE	Pause / Resume
Q	Quit

## Architecture

This project is structured with separation of concerns:

```
game_of_life/
│
├── engine/        # Simulation core
├── gui/           # Pygame interface
├── cli/           # Click-based CLI
├── rules/         # Rule systems
├── board_file/    # Pattern presets
└── main.py        # Entry point
```

Design Goals:

Clean modular architecture

Easy extensibility (new rules / renderers)

Testable simulation engine

Portfolio-grade code quality

## Configuration

The engine supports configuration using the CLI:

```bash
--width INTEGER # Width of the grid.
--height INTEGER # Height of the grid.
--file TEXT # Load an initial pattern from a file path.
--interval FLOAT # Time between generations (in seconds).
--fill-mode TEXT # Cell state when initializing the grid between DEAD and RANDOM.
--placement TEXT # Where to place the loaded file between topleft and center.
--rules [classic|zombie|neumann|respawn] # Rules available
--patterns # Flag that colored the patterns of the grid at each generation
```

## Development

Run tests:
```bash
uv run pytest
```

## Tech Stack

Python 3.12+

pygame (GUI)

click (CLI)

uv (environment management)

pytest (testing)

## Why this project?

This project was built for fun to:

Explore simulation design

Practice clean architecture

Build a portfolio-quality Python project

Experiment with GUI + CLI coexistence

## Contributing

Ideas, issues, and pull requests are welcome!

## License

MIT License
