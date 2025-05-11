from __future__ import annotations

from datetime import datetime

from typing_extensions import TypedDict, TypeAlias, Literal


class Perf(TypedDict):
    games: int
    rating: int
    rd: int
    prog: int
    prov: bool


class Profile(TypedDict):
    """Public profile of an account."""

    flag: str
    location: str
    bio: str
    realName: str
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

    id: str
    username: str
    perfs: dict[str, Perf]
    flair: str
    createdAt: datetime
    disabled: bool
    tosViolation: bool
    profile: Profile
    seenAt: datetime
    patron: bool
    verified: bool
    playTime: PlayTime
    title: str
    url: str
    playing: str
    count: dict[str, int]
    streaming: bool
    streamer: dict[str, StreamerInfo]
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
    "speech"
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
