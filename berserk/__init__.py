# -*- coding: utf-8 -*-
"""Top-level package for berserk."""

from importlib import metadata

berserk_metadata = metadata.metadata(__package__)


__author__ = berserk_metadata["Author"]
__email__ = berserk_metadata["Author-emai"]
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
from .formats import LIJSON
from .formats import NDJSON
from .formats import PGN
