"""Top-level package for berserk."""

from importlib import metadata

berserk_metadata = metadata.metadata(__package__)


__author__ = berserk_metadata["Author"]
__email__ = berserk_metadata["Author-email"]
__version__ = berserk_metadata["Version"]


from .clients import Client
from .types import (
    ArenaResult,
    BroadcastPlayer,
    PaginatedTopBroadcasts,
    Team,
    LightUser,
    ChapterIdName,
    OnlineLightUser,
    OpeningStatistic,
    PaginatedTeams,
    PuzzleRace,
    SwissInfo,
    SwissResult,
    TVFeed,
)
from .session import TokenSession
from .session import Requestor
from .formats import JSON
from .formats import JSON_LIST
from .formats import LIJSON
from .formats import NDJSON
from .formats import NDJSON_LIST
from .formats import PGN

__all__ = [
    "ArenaResult",
    "BroadcastPlayer",
    "PaginatedTopBroadcasts",
    "ChapterIdName",
    "Client",
    "JSON",
    "JSON_LIST",
    "LightUser",
    "LIJSON",
    "NDJSON",
    "NDJSON_LIST",
    "OnlineLightUser",
    "OpeningStatistic",
    "PaginatedTeams",
    "PGN",
    "PuzzleRace",
    "Requestor",
    "SwissInfo",
    "SwissResult",
    "Team",
    "TokenSession",
    "TVFeed",
]
