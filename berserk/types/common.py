from __future__ import annotations

from typing_extensions import Literal, TypedDict, TypeAlias, Union


class ClockConfig(TypedDict):
    # starting time in seconds
    limit: int
    # increment in seconds
    increment: int


Color: TypeAlias = Literal["white", "black"]

GameType: TypeAlias = Literal[
    "chess960",
    "kingOfTheHill",
    "threeCheck",
    "antichess",
    "atomic",
    "horde",
    "racingKings",
    "crazyhouse",
    "fromPosition",
]

Variant: TypeAlias = Union[GameType, Literal["standard"]]

PerfType: TypeAlias = Union[
    GameType, Literal["bullet", "blitz", "rapid", "classical", "ultraBullet"]
]

GameRule: TypeAlias = Literal[
    "noAbort", "noRematch", "noGiveTime", "noClaimWin", "noEarlyDraw"
]

ChallengeDeclineReason: TypeAlias = Literal[
    "generic",
    "later",
    "tooFast",
    "tooSlow",
    "timeControl",
    "rated",
    "casual",
    "standard",
    "variant",
    "noBot",
    "onlyBot",
]
