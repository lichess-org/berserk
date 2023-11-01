from __future__ import annotations

from typing_extensions import TypeAlias, TypedDict, NotRequired, Literal

from .common import Variant, Color, OnlineLightUser
from .opening_explorer import Speed

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

ChallengeDirection: TypeAlias = Literal["in", "out"]


class User(OnlineLightUser):
    """Challenge User"""

    rating: NotRequired[float]
    provisional: NotRequired[bool]


class Challenge(TypedDict):
    """Information about a challenge."""

    id: str
    url: str
    status: ChallengeStatus
    challenger: User
    destUser: User | None
    variant: Variant
    rated: bool
    speed: Speed
    timeControl: object
    color: Color
    perf: str
    direction: NotRequired[ChallengeDirection]
    initialFen: NotRequired[str]
    declineReason: str
    declineReasonKey: str
