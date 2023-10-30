"""Top-level package for berserk."""

from importlib import metadata

berserk_metadata = metadata.metadata(__package__)


__author__ = berserk_metadata["Author"]
__email__ = berserk_metadata["Author-email"]
__version__ = berserk_metadata["Version"]


from .clients import Client
from .types import Team, OpeningStatistic, PaginatedTeams, LightUser, OnlineLightUser
from .session import TokenSession
from .session import Requestor
from .formats import JSON
from .formats import JSON_LIST
from .formats import LIJSON
from .formats import NDJSON
from .formats import NDJSON_LIST
from .formats import PGN

__all__ = [
    "Client",
    "LightUser",
    "OnlineLightUser",
    "TokenSession",
    "Team",
    "PaginatedTeams",
    "OpeningStatistic",
    "Requestor",
    "JSON",
    "JSON_LIST",
    "LIJSON",
    "NDJSON",
    "NDJSON_LIST",
    "PGN",
]
