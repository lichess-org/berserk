from __future__ import annotations

from typing import Union

from typing_extensions import Literal, TypedDict, TypeAlias, NotRequired


class ClockConfig(TypedDict):
    # starting time in seconds
    limit: int
    # increment in seconds
    increment: int


class ExternalEngine(TypedDict):
    # Engine ID
    id: str
    # Engine display name
    name: str
    # Secret token that can be used to request analysis
    clientSecret: str
    # User this engine has been registered for
    userId: str
    # Max number of available threads
    maxThreads: int
    # Max available hash table size, in MiB
    maxHash: int
    # Estimated depth of normal search
    defaultDepth: int
    # List of supported chess variants
    variants: str
    # Arbitrary data that engine provider can use for identification or bookkeeping
    providerData: NotRequired[str]


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

Speed = Literal[
    "ultraBullet", "bullet", "blitz", "rapid", "classical", "correspondence"
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
    # The flair of the user
    flair: NotRequired[str]
    # The patron of the user
    patron: NotRequired[bool]


class OnlineLightUser(LightUser):
    # Whether the user is online
    online: NotRequired[bool]


VariantKey: TypeAlias = Union[
    GameType,
    Literal["standard"]
]

PerfType: TypeAlias = Union[
    GameType, Literal["bullet", "blitz", "rapid", "classical", "ultraBullet"]
]

GameRule: TypeAlias = Literal[
    "noAbort", "noRematch", "noGiveTime", "noClaimWin", "noEarlyDraw"
]
