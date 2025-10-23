from __future__ import annotations

from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict

from .common import LightUser, Title


class BroadcastPlayer(TypedDict):
    # The name of the player as it appears on the source PGN
    source_name: str
    # The name of the player as it will be displayed on Lichess
    display_name: str
    # Rating, optional
    rating: NotRequired[int]
    # Title, optional
    title: NotRequired[Title]


class BroadcastTourInfoInfo(TypedDict, total=False):
    website: NotRequired[str]
    players: NotRequired[str]
    location: NotRequired[str]
    tc: NotRequired[str]
    fideTc: NotRequired[str]
    timeZone: NotRequired[str]
    standings: NotRequired[str]
    format: NotRequired[str]


class BroadcastTourInfo(TypedDict, total=False):
    id: str
    name: str
    slug: str
    createdAt: int
    dates: NotRequired[List[int]]
    info: NotRequired[BroadcastTourInfoInfo]
    tier: NotRequired[int]
    image: NotRequired[str]
    description: NotRequired[str]
    leaderboard: NotRequired[bool]
    teamTable: NotRequired[bool]
    url: str
    communityOwner: NotRequired[LightUser]


class BroadcastRoundInfo(TypedDict, total=False):
    id: str
    name: str
    slug: str
    createdAt: int
    rated: bool
    ongoing: NotRequired[bool]
    startsAt: NotRequired[int]
    startsAfterPrevious: NotRequired[bool]
    finishedAt: NotRequired[int]
    finished: NotRequired[bool]
    url: str
    delay: NotRequired[int]
    customScoring: NotRequired[Dict[str, Any]]


class BroadcastWithLastRound(TypedDict, total=False):
    group: NotRequired[str]
    tour: BroadcastTourInfo
    round: BroadcastRoundInfo
    roundToLink: NotRequired[BroadcastRoundInfo]


class BroadcastPastPage(TypedDict, total=False):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[BroadcastWithLastRound]
    previousPage: NotRequired[int | None]
    nextPage: NotRequired[int | None]


class BroadcastTopResponse(TypedDict):
    active: List[BroadcastWithLastRound]
    upcoming: List[BroadcastWithLastRound]
    past: BroadcastPastPage
