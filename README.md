## Project Description
This project is a Python-based simulation of the classic Battleship game. It includes modules for creating and managing the game board, players, ships, and game logic. The project allows for various simulations, including automatic and manual player modes.

## Project Structure

```
Project folder/
├─ battleship/
│  ├─ board.py
│  ├─ convert.py
│  ├─ game.py
│  ├─ player.py
│  ├─ ship.py
│  ├─ simulation.py
├─ tests/
│  ├─ test_board.py
│  ├─ test_player.py
│  ├─ test_ship.py
│  ├─ test_shipfactory.py
├─ main.py
```


### `battleship/`

- `board.py` represents a player's game board and manages the ships on it.

- `convert.py` utility class for converting cell coordinates between different formats.

- `game.py` core class for the game logic, including handling hits and game outcomes.

- `player.py` contains the `Player`, `ManualPlayer`, and `RandomPlayer` classes, handling their board and moves.

- `ship.py` contains the `Ship` class and the `ShipFactory` class, creating multiple ships where each ship has a defined position and status on the game board.

- `simulation.py` contains classes for different game simulations


### `tests/`

Contains an example test case for each of the four tasks.

- `test_board.py`
- `test_player.py`
- `test_ship.py`
- `test_shipfactory.py`

You can run the test via `python3 -m tests.test_board` (and similarly for the other tests).


### `main.py`

Allows you to run a simulation of a battleship game.

Running `python3 main.py` or `python3 main.py 0` will give you a manual game between two humans.

Running `python3 main.py 1` will give you a manual game between a human and a `RandomPlayer`.

