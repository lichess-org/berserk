"""Top-level package for berserk."""

from importlib import metadata

berserk_metadata = metadata.metadata(__package__)


__author__ = berserk_metadata["Author"]
__email__ = berserk_metadata["Author-email"]
__version__ = berserk_metadata["Version"]


from .clients import Client
from .session import TokenSession
from .session import Requestor
from .enums import PerfType
from .enums import Variant
from .enums import Color
from .enums import Room
from .enums import Mode
from .enums import Position
from .enums import Reason
from .formats import JSON
from .formats import JSON_LIST
from .formats import LIJSON
from .formats import NDJSON
from .formats import NDJSON_LIST
from .formats import PGN

__all__ = [
    "Client",
    "TokenSession",
    "Requestor",
    "PerfType",
    "Variant",
    "Color",
    "Room",
    "Mode",
    "Position",
    "Reason",
    "JSON",
    "JSON_LIST",
    "LIJSON",
    "NDJSON",
    "NDJSON_LIST",
    "PGN",
]
