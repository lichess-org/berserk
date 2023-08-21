"""Aliases for account endpoints."""
from __future__ import annotations

from datetime import datetime

from typing_extensions import TypedDict

from ..enums import AllPerfType, CountTypes, StreamingService


class Perf(TypedDict):
    """A perf."""

    games: int
    rating: int
    rd: int
    prog: int
    prov: bool


class PlayTime(TypedDict):
    """Account play time."""

    total: int
    tv: int


class Profile(TypedDict):
    """Public profile of an account."""

    country: str
    location: str
    bio: str
    firstName: str
    lastName: str
    fideRating: int
    uscfRating: int
    ecfRating: int
    links: str


class StreamerInfo(TypedDict):
    """Information about the streamer on a given platform."""

    channel: str


class AccountInformation(TypedDict):
    """Informations about an account."""

    id: str
    username: str
    perfs: dict[AllPerfType, Perf]
    createdAt: datetime
    disabled: bool
    tosViolation: bool
    profile: Profile
    seenAt: datetime
    patron: bool
    verified: bool
    title: str
    url: str
    playing: str
    count: dict[CountTypes, int]
    streaming: bool
    streamer: dict[StreamingService, StreamingService]
    followable: bool
    following: bool
    blocking: bool
    followsYou: bool


class Prefs(TypedDict):
    """User settings."""

    dark: bool
    transp: bool
    bgImg: str
    is3d: bool
    theme: str
    pieceSet: str
    theme3d: str
    pieceSet3d: str
    soundSet: str
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
    """Preferences of an account."""

    prefs: Prefs
    language: str
