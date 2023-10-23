from __future__ import annotations

from typing import Union, Literal

from typing_extensions import Literal, TypedDict, TypeAlias, NotRequired


class ClockConfig(TypedDict):
    # starting time in seconds
    limit: int
    # increment in seconds
    increment: int


class PuzzleRace(TypedDict):
    # Puzzle race ID
    id: str
    # Puzzle race URL
    url: str


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

Title = Literal[
    "GM", "WGM", "IM", "WIM", "FM", "WFM", "NM", "CM", "WCM", "WNM", "LM", "BOT"
]


class LightUser(TypedDict):
    # The id of the user
    id: str
    # The name of the user
    name: str
    # The title of the user
    title: NotRequired[Title]
    # The patron of the user
    patron: NotRequired[bool]


class OnlineLightUser(LightUser):
    # Whether the user is online
    online: NotRequired[bool]


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
