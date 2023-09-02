from __future__ import annotations

from typing import Literal

from typing_extensions import TypedDict, TypeAlias


class ClockConfig(TypedDict):
    # starting time in seconds
    limit: int
    # increment in seconds
    increment: int


Variant: TypeAlias = Literal[
    "standard",
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

GameRule: TypeAlias = Literal[
    "noAbort", "noRematch", "noGiveTime", "noClaimWin", "noEarlyDraw"
]
