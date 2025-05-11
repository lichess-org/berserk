from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias, TypedDict, Required, NotRequired, Literal

from .common import VariantKey, Color, OnlineLightUser, Speed

ChallengeStatus: TypeAlias = Literal[
    "created",
    "offline",
    "canceled",
    "declined",
    "accepted",
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

ColorOrRandom: TypeAlias = Union[
    Color, Literal["random"]
]

ChallengeDirection: TypeAlias = Literal["in", "out"]


class Variant(TypedDict):
    key: VariantKey
    name: str
    short: str


class User(OnlineLightUser):
    """Challenge User"""

    rating: NotRequired[float]
    provisional: NotRequired[bool]


class Perf(TypedDict):
    icon: str
    name: str


class ChallengeJson(TypedDict):
    """Information about a challenge."""

    id: Required[str]
    url: Required[str]
    status: Required[ChallengeStatus]
    challenger: Required[User]
    destUser: Required[User | None]
    variant: Required[Variant]
    rated: Required[bool]
    speed: Required[Speed]
    timeControl: object
    color: Required[ColorOrRandom]
    finalColor: Color
    perf: Required[Perf]
    direction: NotRequired[ChallengeDirection]
    initialFen: NotRequired[str]
    declineReason: str
    declineReasonKey: str
