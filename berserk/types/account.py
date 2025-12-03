from __future__ import annotations

from datetime import datetime

from typing_extensions import TypedDict, TypeAlias, Literal, NotRequired, Union
from .common import LightUser, PerfType, Title


class Perf(TypedDict):
    games: int
    rating: int
    rd: int
    prog: int
    prov: NotRequired[bool]


class Profile(TypedDict):
    """Public profile of an account."""

    flag: NotRequired[str]
    location: NotRequired[str]
    bio: str
    realName: NotRequired[str]
    fideRating: int
    uscfRating: int
    ecfRating: int
    cfcRating: int
    rcfRating: int
    dsbRating: int
    links: str


class PlayTime(TypedDict):
    total: int
    tv: int


class StreamerInfo(TypedDict):
    """Information about the streamer on a specific platform."""

    channel: str


class AccountInformation(TypedDict):
    """Information about an account."""

    # Same as Light user except name <-> username

    # The id of the user
    id: str
    # The name of the user
    username: str
    # The title of the user
    title: NotRequired[Title]
    # The flair of the user
    flair: NotRequired[str]
    # The patron of the user
    patron: NotRequired[bool]
    # The patron color of the user
    patronColor: NotRequired[int]

    perfs: dict[str, Perf]
    createdAt: datetime
    disabled: NotRequired[bool]
    tosViolation: NotRequired[bool]
    profile: Profile
    seenAt: datetime
    verified: NotRequired[bool]
    playTime: PlayTime
    url: str
    playing: NotRequired[str]
    count: dict[str, int]
    streaming: NotRequired[bool]
    streamer: NotRequired[dict[str, StreamerInfo]]
    followable: bool
    following: bool
    blocking: bool


SoundSet: TypeAlias = Literal[
    "silent",
    "standard",
    "piano",
    "nes",
    "sfx",
    "futuristic",
    "robot",
    "music",
    "speech",
]


class UserPreferences(TypedDict, total=False):
    dark: bool
    transp: bool
    bgImg: str
    is3d: bool
    theme: str
    pieceSet: str
    theme3d: str
    pieceSet3d: str
    soundSet: SoundSet
    blindfold: int
    autoQueen: int
    autoThreefold: int
    takeback: int
    moretime: int
    clockTenths: int
    clockBar: bool
    clockSound: bool
    premove: bool
    animation: int
    captured: bool
    follow: bool
    highlight: bool
    destination: bool
    coords: int
    replay: int
    challenge: int
    message: int
    coordColor: int
    submitMove: int
    confirmResign: int
    insightShare: int
    keyboardMove: int
    zen: int
    moveEvent: int
    rookCastle: int


class Preferences(TypedDict):
    prefs: UserPreferences
    language: str


# from lila/modules/core/src/main/timeline.scala


class TimelineEntry(TypedDict):
    date: datetime


# ---


class FollowEntry(TimelineEntry):
    data: FollowData
    type: Literal["follow"]


class FollowData(TypedDict):
    u1: str
    u2: str


# ---


class TeamJoinEntry(TimelineEntry):
    data: TeamJoinData
    type: Literal["team-join"]


class TeamJoinData(TypedDict):
    userId: str
    teamId: str


# ---


class TeamCreateEntry(TimelineEntry):
    data: TeamCreateData
    type: Literal["team-create"]


class TeamCreateData(TypedDict):
    userId: str
    teamId: str


# ---


class ForumPostEntry(TimelineEntry):
    data: ForumPostData
    type: Literal["forum-post"]


class ForumPostData(TypedDict):
    userId: str
    topicId: str
    topicName: str
    postId: str


# ---


class UblogPostEntry(TimelineEntry):
    data: UblogPostData
    type: Literal["ublog-post", "ublog-post-like"]


class UblogPostData(TypedDict):
    userId: str
    id: str
    title: str


# ---


class TourJoinEntry(TimelineEntry):
    data: TourJoinData
    type: Literal["tour-join"]


class TourJoinData(TypedDict):
    userId: str
    tourId: str
    tourName: str


# ---


class GameEndEntry(TimelineEntry):
    data: GameEndData
    type: Literal["game-end"]


class GameEndData(TypedDict):
    fullId: str
    opponent: NotRequired[str]
    win: NotRequired[bool]
    perf: PerfType


# ---


class SimulEntry(TimelineEntry):
    data: SimulData
    type: Literal["simul-create", "simul-join"]


class SimulData(TypedDict):
    userId: str
    simulId: str
    simulName: str


# ---


class StudyLikeEntry(TimelineEntry):
    data: StudyLikeData
    type: Literal["study-like"]


class StudyLikeData(TypedDict):
    userId: str
    studyId: str
    studyName: str


# ---


class PlanStartEntry(TimelineEntry):
    data: PlanStartData
    type: Literal["plan-start"]


class PlanStartData(TypedDict):
    userId: str


# ---


class PlanRenewEntry(TimelineEntry):
    data: PlanRenewData
    type: Literal["plan-renew"]


class PlanRenewData(TypedDict):
    userId: str
    months: int


# ---

TimelineEntries = Union[
    FollowEntry,
    TeamJoinEntry,
    TeamCreateEntry,
    ForumPostEntry,
    UblogPostEntry,
    TourJoinEntry,
    GameEndEntry,
    StudyLikeEntry,
    SimulEntry,
    PlanStartEntry,
    PlanRenewEntry,
]


class Timeline(TypedDict):
    entries: list[TimelineEntries]
    users: dict[str, LightUser]
