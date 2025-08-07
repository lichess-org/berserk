from __future__ import annotations

from typing import Union
from typing_extensions import TypedDict, Literal, TypeAlias

from .account import Perf
from .challenges import ChallengeStatus, ChallengeJson
from .common import Color, Speed


GameSource: TypeAlias = Literal[
    "lobby",
    "friend",
    "ai",
    "api",
    "tournament",
    "position",
    "import",
    "importlive",
    "simul",
    "relay",
    "pool",
    "swiss",
]


class Opponent(TypedDict):
    id: str
    username: str
    rating: int


class GameEventInfo(TypedDict):
    fullId: str
    gameId: str
    fen: str
    color: Color
    lastMove: str
    source: GameSource
    status: ChallengeStatus
    variant: object
    speed: Speed
    perf: Perf
    rated: bool
    hasMoved: bool
    opponent: Opponent
    isMyTurn: bool
    secondsLeft: int
    compat: object
    id: str


class GameEvent(TypedDict):
    type: Literal["gameStart", "gameFinish"]
    game: GameEventInfo


class ChallengeEvent(TypedDict):
    type: Literal["challenge", "challengeCanceled", "challengeDeclined"]
    challenge: ChallengeJson


IncomingEvent: TypeAlias = Union[
    GameEvent,
    ChallengeEvent,
]
