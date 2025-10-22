from __future__ import annotations

from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict

from .common import Title


class BroadcastPlayer(TypedDict):
    # The name of the player as it appears on the source PGN
    source_name: str
    # The name of the player as it will be displayed on Lichess
    display_name: str
    # Rating, optional
    rating: NotRequired[int]
    # Title, optional
    title: NotRequired[Title]


class BroadcastTopResponse(TypedDict):
    """Minimal TypedDict for /api/broadcast/top response."""

    # List of active broadcasts
    active: List[Dict[str, Any]]
    # List of upcoming broadcasts
    upcoming: List[Dict[str, Any]]
    # List of past broadcasts
    past: Dict[str, Any]
