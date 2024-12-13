from __future__ import annotations
from typing import List, Dict, Optional, Any
from typing_extensions import NotRequired, TypedDict

from .common import Title


class BroadcastPlayer(TypedDict):
    # The name of the player as it appears on the source PGN
    source_name: str
    # The name of the player as it will be displayed on Lichess
    display_name: str
    # Rating, optional
    rating: NotRequired[int]
    # Title, optional
    title: NotRequired[Title]


# top broadcasts start here


class PaginatedTopBroadcasts(TypedDict):
    # active broadcasts
    active: List[BroadcastWithLastRound]
    # upcoming broadcasts
    upcoming: List[BroadcastWithLastRound]
    # pagination meta data
    past: BroadcastPaginationMetadata


class BroadcastWithLastRound(TypedDict, total=False):
    # group of broadcast
    group: str
    # broadcast round
    round: BroadcastRoundInfo
    # broadcast tour
    tour: BroadcastTour
    # not listed in docs currently
    roundToLink: Dict[str, Any]


class BroadcastPaginationMetadata(TypedDict, total=False):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[Dict[str, Any]]
    previousPage: Optional[int]
    nextPage: Optional[int]


class BroadcastTour(TypedDict, total=False):
    id: str
    name: str
    slug: str
    createdAt: int
    # Start and end dates of the tournament, as Unix timestamps in milliseconds
    dates: Optional[List[int]]
    # Additional display information about the tournament
    info: BroadcastTourInfo
    # Used to designate featured tournaments on Lichess
    tier: Optional[int]
    image: Optional[str]
    # Full tournament description in markdown format, or in HTML if the html=1 query parameter is set.
    description: Optional[str]
    leaderboard: Optional[bool]
    teamTable: Optional[bool]
    url: str


class BroadcastTourInfo(TypedDict, total=False):
    # Official website. External website URL
    website: str
    # Featured players
    players: str
    # Tournament location
    location: str
    # Time control
    tc: str
    # FIDE rating category
    fideTc: str
    # Timezone of the tournament. Example: America/New_York.
    timeZone: str
    # Official standings website. External website URL
    standings: str
    # Tournament format
    format: str


class BroadcastRoundInfo(TypedDict, total=False):
    id: str
    name: str
    slug: str
    createdAt: int
    ongoing: Optional[bool]
    startsAt: Optional[int]
    # The start date/time is unknown and the round will start automatically when the previous round completes
    startsAfterPrevious: Optional[bool]
    finishedAt: Optional[int]
    url: str
    delay: Optional[int]
