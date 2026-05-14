# Candy Crush

A simple Candy Crush-like puzzle game implemented in Python with Pygame. Features smooth animations for swapping and disappearing tiles, cascading matches, and score tracking.

## Features

- **8×8 game grid** with colorful tiles
- **Smooth animations**:
  - Tile swapping with fluid motion
  - Disappearing animation when tiles match
  - Falling animation when tiles drop
  - Spawning animation for new tiles
- **Match detection**: Automatically detect 3+ tiles in a row/column
- **Cascading matches**: Chain reactions when new tiles fall into position
- **Score system**: Earn 10 points per matched tile
- **6 different tile colors**: Red, Green, Blue, Yellow, Orange, Magenta

## Gameplay

1. **Select a tile** by clicking on it (a white circle appears)
2. **Click an adjacent tile** to swap them
3. **Match 3+ tiles** of the same color horizontally or vertically
4. **Matched tiles disappear** and points are awarded
5. **Tiles fall** to fill empty spaces
6. **New tiles spawn** from the top to continue playing

## Requirements

- Python 3.7+
- Pygame 2.5.2

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/candycrush.git
cd candycrush
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python candy_crush.py
```

The game window will open and you can start playing immediately!

## Controls

- **Left Click**: Select and swap tiles
- **Close Window**: Exit the game

## Game Mechanics

- **Scoring**: Each matched tile awards 10 points
- **Valid Moves**: You can only swap adjacent tiles (horizontally or vertically)
- **Auto-Fill**: After matches are cleared, tiles automatically fall and new ones spawn
- **Cascades**: If new tiles create matches, they automatically clear in chain reactions

## Project Structure

```
candycrush/
├── candy_crush.py      # Main game code
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

This project is open source and available under the MIT License.

## Credits

Created as a fun puzzle game implementation in Python.
