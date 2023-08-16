"""Common types"""
from __future__ import annotations

from typing_extensions import TypedDict, NotRequired


class Result(TypedDict):
    """Operation result"""

    ok: NotRequired[bool]
    error: NotRequired[str]
