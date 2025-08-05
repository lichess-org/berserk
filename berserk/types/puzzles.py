from __future__ import annotations

from enum import Enum

from typing_extensions import TypedDict


class PuzzleRace(TypedDict):
    # Puzzle race ID
    id: str
    # Puzzle race URL
    url: str


class Difficulty(str, Enum):
    EASIEST = "easiest"
    EASIER = "easier"
    NORMAL = "normal"
    HARDER = "harder"
    HARDEST = "hardest"
