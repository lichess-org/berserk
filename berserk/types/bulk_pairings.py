from __future__ import annotations

from typing_extensions import TypedDict

from .common import ClockConfig, VariantKey


class BulkPairingGame(TypedDict):
    id: str
    black: str
    white: str


class BulkPairing(TypedDict):
    id: str
    games: list[BulkPairingGame]
    variant: VariantKey
    clock: ClockConfig
    pairAt: int
    pairedAt: int | None
    rated: bool
    startClocksAt: int
    scheduledAt: int
