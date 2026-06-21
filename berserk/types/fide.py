from __future__ import annotations
from typing import List
from typing_extensions import NotRequired, TypedDict


class FidePlayer(TypedDict):
    id: int
    name: str
    federation: str
    year: int
    title: NotRequired[str]
    standard: NotRequired[int]
    rapid: NotRequired[int]
    blitz: NotRequired[int]


class FidePlayerRatings(TypedDict):
    """Historical FIDE ratings of a player.

    Each list contains encoded data points where a single number packs a
    year, month, and ELO rating (e.g. `2015081568` -> August 2015, 1568).
    Consecutive months with the same rating are omitted; only the first and
    last month of an unchanged stretch are included.
    """

    standard: List[int]
    rapid: List[int]
    blitz: List[int]
