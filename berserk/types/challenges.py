from __future__ import annotations

from typing_extensions import TypedDict, NotRequired, TypeAlias, Literal


Status: TypeAlias = Literal[
    "created",
    "offline",
    "canceled",
    "declined",
    "accepted",
]


Title: TypeAlias = Literal[
    "GM",
    "WGM",
    "IM",
    "WIM",
    "FM",
    "WFM",
    "NM",
    "CM",
    "WCM",
    "WNM",
    "LM",
    "BOT",
]


class User(TypedDict):
    """Challenge User"""

    rating: NotRequired[float]
    provisional: NotRequired[bool]
    online: NotRequired[bool]
    id: str
    name: str
    title: NotRequired[Title]
    patron: NotRequired[bool]


VariantKey: TypeAlias = Literal[
    "standard",
    "chess960",
    "crazyhouse",
    "antichess",
    "atomic",
    "horde",
    "kingOfTheHill",
    "racingKings",
    "threeCheck",
    "fromPosition",
]


class Variant(TypedDict):
    """Information about a challenge variant."""

    key: NotRequired[VariantKey]
    name: NotRequired[str]
    short: NotRequired[str]


Speed: TypeAlias = Literal[
    "ultraBullet",
    "bullet",
    "blitz",
    "rapid",
    "classical",
    "correspondence",
]


Color: TypeAlias = Literal[
    "white",
    "black",
    "random",
]

Direction: TypeAlias = Literal[
    "in",
    "out",
]


DeclineReason: TypeAlias = Literal[
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


class Challenge(TypedDict):
    """Information about a challenge."""

    id: str
    url: str
    status: Status
    challenger: User
    destUser: User | None
    variant: Variant
    rated: bool
    speed: Speed
    timeControl: object
    color: Color
    perf: str
    direction: NotRequired[Direction]
    initialFen: NotRequired[str]
    declineReason: str
    declineReasonKey: str
