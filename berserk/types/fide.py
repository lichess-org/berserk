from __future__ import annotations
from typing import List
from typing_extensions import NotRequired,TypedDict


class FidePlayer(TypedDict):
    id: int
    name: str
    federation: str
    year: int
    title: NotRequired[str]
    standard: NotRequired[int]
    rapid: NotRequired[int]
    blitz: NotRequired[int]
