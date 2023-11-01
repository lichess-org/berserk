from __future__ import annotations

from typing_extensions import TypedDict, NotRequired
from common import ChallengeStatus, Color, Title, Variant, ChallengeDirection
from opening_explorer import Speed


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
