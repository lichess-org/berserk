from __future__ import annotations

from typing import List
from typing_extensions import TypedDict, NotRequired

from .common import LightUser


class PuzzleGame(TypedDict):
    # Game ID from which the puzzle was extracted
    id: str
    # Full PGN of the game
    pgn: str
    # Time control used in the game
    clock: str


class Puzzle(TypedDict):
    # Puzzle unique identifier
    id: str
    # FEN position for the puzzle
    fen: str
    # Array of moves (the solution)
    moves: List[str]  
    # Puzzle difficulty rating
    rating: int
    # Number of times the puzzle has been attempted
    plays: int
    # Puzzle themes/tags
    themes: List[str]
    # Information about the source game
    game: PuzzleGame
    # Initial move that sets up the puzzle position (optional)
    initialMove: NotRequired[str]
    # Solution moves (optional, might be same as moves)
    solution: NotRequired[List[str]]


class PuzzleRace(TypedDict):
    # Puzzle race ID
    id: str
    # Puzzle race URL
    url: str
