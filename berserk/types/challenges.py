from __future__ import annotations

from typing_extensions import TypedDict, NotRequired, TypeAlias, Literal
from common import Color, Title, Variant
from opening_explorer import Speed

Status: TypeAlias = Literal[
    "created",
    "offline",
    "canceled",
    "declined",
    "accepted",
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


class User(TypedDict):
    """Challenge User"""

    rating: NotRequired[float]
    provisional: NotRequired[bool]
    online: NotRequired[bool]
    id: str
    name: str
    title: NotRequired[Title]
    patron: NotRequired[bool]


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
