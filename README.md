# Billiard Club

A 2D pool/billiards game built with **Python** and **Pygame**, made as my A Level Computer Science Non-Exam Assessment (NEA) project, completed for the 2025 exam series.

The game features full 8-ball pool logic, realistic ball physics, a basic AI opponent, and a complete menu system with sound and customisation options.

## Features

- **8-ball pool rules** — turn tracking, ball type assignment (spots/stripes), potting, fouls, and win detection
- **Realistic physics** — ball-to-ball and ball-to-wall collisions, friction, and restitution
- **Multiple game modes** — Player vs Player, Player vs AI, and a free-play Sandbox mode
- **Basic AI opponent** — the computer selects and takes shots automatically
- **Full menu system** — main menu, game mode selection, options, pause, and win screens
- **Customisation** — player names and ball colours
- **Audio** — background music and sound effects for shots, collisions, and potted balls, with volume controls
- **UI extras** — power slider for shots, ball indicator UI, player turn indicator, FPS counter, and a blurred menu background effect

## Project Structure

```
Project/
├── src/
│   └── main.py          # Main game source code
├── example/              # Early prototypes used during development
│   ├── ballPhysics.py
│   └── sliders.py
├── img/                   # Image assets
└── other/                 # Fonts and audio assets
```

## Requirements

- Python 3
- [Pygame](https://www.pygame.org/)
- [NumPy](https://numpy.org/)
- [OpenCV](https://opencv.org/) (`opencv-python`)

Install dependencies with:

```bash
pip install pygame numpy opencv-python
```

## Running the Game

Run the game from the **repository root** (asset paths are relative to it):

```bash
python Project/src/main.py
```

## Controls

- **Mouse** — aim the cue and use the power slider to control shot strength
- **Left Click** — take a shot
- **Esc** — pause the game

## Notes

This project was built as a solo A Level NEA submission, with a focus on demonstrating object-oriented programming, vector-based physics, and event-driven UI design in Pygame.
