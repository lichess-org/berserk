"""Aliases for bulk pairings endpoints"""
from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .core.aliases import ID, Username


class BulkPairingGame(TypedDict):
    """A bulk pairing game"""

    id: ID
    black: Username
    white: Username


class BulkPairingClock(TypedDict):
    """A bulk pairing clock"""

    increment: int
    limit: int


class BulkPairing(TypedDict):
    """Represents a bulk pairing."""

    id: ID
    games: List[BulkPairingGame]
    clock: BulkPairingClock
    pairAt: int
    pairedAt: None
    rated: bool
    startClocksAt: int
    scheduledAt: int
