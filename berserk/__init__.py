# -*- coding: utf-8 -*-
"""Top-level package for berserk."""

from importlib import metadata

berserk_metadata = metadata.metadata(__package__)


__author__ = berserk_metadata["Author"]
__email__ = berserk_metadata["Author-emai"]
__version__ = berserk_metadata["Version"]


from .clients import Client  # noqa: F401
from .session import TokenSession  # noqa: F401
from .session import Requestor  # noqa: F401
from .enums import PerfType  # noqa: F401
from .enums import Variant  # noqa: F401
from .enums import Color  # noqa: F401
from .enums import Room  # noqa: F401
from .enums import Mode  # noqa: F401
from .enums import Position  # noqa: F401
from .enums import Reason  # noqa: F401
from .formats import JSON  # noqa: F401
from .formats import LIJSON  # noqa: F401
from .formats import NDJSON  # noqa: F401
from .formats import PGN  # noqa: F401
