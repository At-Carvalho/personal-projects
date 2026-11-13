# 💣 Bomberman Clone

A simple **Bomberman-inspired game** developed in Python using Pygame as a programming project.

Navigate through a destructible maze, avoid explosions, and defeat the enemy using strategically placed bombs!

## 🎮 Features

- **Procedurally Generated Maps** – Each new game creates a randomly generated map.
- **Destructible Environments** – Breakable and indestructible walls.
- **Bomb Mechanics** – Place bombs with a timed detonation system.
- **Explosion System** – Explosions spread horizontally and vertically, stopping at walls.
- **Enemy AI** – An enemy that moves around the map, detects threats, avoids explosions, and attempts to attack the player.
- **Game States** – Main menu, pause menu, victory screen, and defeat screen.
- **Collision Detection** – Walls and bombs prevent movement.

## 🕹️ Controls

| Key | Action |
|---|---|
| `W` / `↑` | Move up |
| `A` / `←` | Move left |
| `S` / `↓` | Move down |
| `D` / `→` | Move right |
| `SPACE` | Place a bomb / Select menu option |
| `ESC` | Pause / Resume / Return to main menu |

## 🛠️ Technologies

- **Python 3**
- **Pygame**

## 📁 Project Structure

The project is organized into five Python files, separating configuration, map generation, game logic, rendering, and the main game loop.

```text
Bomberman-Clone/
│
├── main.py       # Main game loop and event handling
├── config.py     # Game settings, constants, and colors
├── mapa.py       # Map generation
├── logica.py     # Bombs, explosions, movement validation and enemy AI
├── desenho.py    # Game rendering and menus
│
└── README.md
```

## 🚀 Getting Started

### Requirements

Make sure you have Python installed.

Install Pygame:

```bash
pip install pygame
```

### Running the Game

Clone this repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Navigate to the project folder:

```bash
cd YOUR-REPOSITORY
```

Run the game:

```bash
python main.py
```

## ⚙️ Configuration

Several gameplay parameters can be adjusted in `config.py`, including:

- Map dimensions
- Tile size
- Breakable wall spawn rate
- Bomb explosion timer
- Explosion duration
- Bomb range
- Enemy decision intervals

## 📚 About the Project

This project was developed as part of my learning journey in **Python programming and game development**.

The main goal was to practice programming fundamentals, including:

- Modular code organization
- Functions and data structures
- Game loops and event handling
- Collision detection
- Basic enemy AI
- Time-based game mechanics

## 📄 License

This project is open-source. Feel free to explore the code, learn from it, and adapt it for your own projects.
