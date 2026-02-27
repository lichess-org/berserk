from __future__ import annotations

from typing import List

from typing_extensions import NotRequired, TypedDict, Required

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


class BroadcastTourInfo(TypedDict):
    website: NotRequired[str]
    players: NotRequired[str]
    location: NotRequired[str]
    tc: NotRequired[str]
    fideTc: NotRequired[str]
    timeZone: NotRequired[str]
    standings: NotRequired[str]
    format: NotRequired[str]


class BroadcastTour(TypedDict):
    id: str
    name: str
    slug: str
    createdAt: int
    dates: NotRequired[List[int]]
    info: NotRequired[BroadcastTourInfo]
    tier: NotRequired[int]
    image: NotRequired[str]
    description: NotRequired[str]
    leaderboard: NotRequired[bool]
    teamTable: NotRequired[bool]
    url: str
    communityOwner: NotRequired[LightUser]


class BroadcastCustomPointsPerColor(TypedDict):
    win: float
    draw: float


class BroadcastCustomScoring(TypedDict):
    white: BroadcastCustomPointsPerColor
    black: BroadcastCustomPointsPerColor


class BroadcastRoundInfo(TypedDict):
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
    url: NotRequired[str]
    delay: NotRequired[int]
    customScoring: NotRequired[BroadcastCustomScoring]


class BroadcastWithLastRound(TypedDict):
    group: NotRequired[str]
    tour: BroadcastTour
    round: BroadcastRoundInfo
    roundToLink: NotRequired[BroadcastRoundInfo]


class PaginatedBroadcasts(TypedDict):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[BroadcastWithLastRound]
    previousPage: NotRequired[int | None]
    nextPage: NotRequired[int | None]


class BroadcastTop(TypedDict):
    active: List[BroadcastWithLastRound]
    upcoming: List[None]  # deprecated
    past: PaginatedBroadcasts


class BroadcastByUser(TypedDict):
    tour: BroadcastTour


class BroadcastsByUser(TypedDict):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[BroadcastByUser]
    nbResults: int
    previousPage: int | None
    nextPage: int | None
    nbPages: int


class StatByFideTC(TypedDict, total=False):
    """Rating/performance stats by FIDE time control."""

    standard: int
    rapid: int
    blitz: int


class BroadcastPlayerTiebreak(TypedDict):
    """A single tiebreak value."""

    name: str
    value: float


class BroadcastPlayerWithFed(TypedDict):
    """Base player info with federation."""

    name: str
    title: NotRequired[Title]
    rating: NotRequired[int]
    fideId: NotRequired[int]
    fed: NotRequired[str]


class BroadcastPlayerEntry(BroadcastPlayerWithFed):
    """Player entry in a broadcast leaderboard."""

    score: NotRequired[float]
    played: NotRequired[int]
    ratingDiff: NotRequired[int]  # deprecated
    ratingDiffs: NotRequired[StatByFideTC]
    ratingsMap: NotRequired[StatByFideTC]
    performance: NotRequired[int]  # deprecated
    performances: NotRequired[StatByFideTC]
    tiebreaks: NotRequired[List[BroadcastPlayerTiebreak]]
    rank: NotRequired[int]
    team: NotRequired[str]


class BroadcastGameEntry(TypedDict):
    """A game played by a broadcast player."""

    id: str
    round: NotRequired[str]
    opponent: NotRequired[BroadcastPlayerWithFed]
    color: NotRequired[str]
    result: NotRequired[str]
    ratingDiff: NotRequired[int]


class BroadcastPlayerFideInfo(TypedDict):
    """FIDE info for a broadcast player."""

    year: NotRequired[int]
    ratings: NotRequired[StatByFideTC]


class BroadcastPlayerEntryWithFideAndGames(BroadcastPlayerEntry):
    """Player entry with FIDE data and games."""

    fide: NotRequired[BroadcastPlayerFideInfo]
    games: NotRequired[List[BroadcastGameEntry]]


class BroadcastTeamLeaderboardEntry(TypedDict):
    """Team entry in a broadcast team leaderboard."""

    name: str
    mp: float
    gp: float
    averageRating: NotRequired[int]
    matches: Required[List[dict]]
    players: Required[List[dict]]
