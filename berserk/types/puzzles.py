from __future__ import annotations

from typing_extensions import TypedDict, List

from .common import LightUser, ClockConfig


class PuzzleInfo(TypedDict):
    """Structure containing information about a specific puzzle."""

    id: str
    rating: int
    plays: int
    solution: List[str]
    themes: List[str]
    initialFen: str
    initialPly: int
    gameId: str


class PuzzleGame(TypedDict):
    """Structure containing information about the game the puzzle originated from."""

    id: str
    clock: ClockConfig
    perf: str
    pgn: str
    players: List[LightUser]
    rated: bool


class NextPuzzle(TypedDict):
    """Structure representing the response for the next puzzle request."""

    puzzle: PuzzleInfo
    game: PuzzleGame


class PuzzleRace(TypedDict):
    # Puzzle race ID
    id: str
    # Puzzle race URL
    url: str
