from __future__ import annotations

from typing import List, Literal
from typing_extensions import TypedDict, NotRequired

from .common import LightUser, Color


class Player(TypedDict):
    color: Color
    user: NotRequired[LightUser]
    ai: NotRequired[int]
    rating: NotRequired[int]
    seconds: int


class FeaturedData(TypedDict):
    id: str
    orientation: Color
    players: List[Player]
    fen: str


class MoveData(TypedDict):
    fen: str
    lm: str
    wc: int
    bc: int


class TVFeed(TypedDict):
    t: Literal["featured", "fen"]
    d: FeaturedData | MoveData
