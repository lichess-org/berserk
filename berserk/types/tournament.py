from typing import TypedDict, Union


class Clock(TypedDict):
    limit: int
    increment: int


class Stats(TypedDict):
    absences: int
    averageRating: int
    blackWins: int
    byes: int
    draws: int
    games: int
    whiteWins: int


class SwissInfo(TypedDict):
    id: str
    createdBy: str
    startsAt: str
    name: str
    clock: Clock
    variant: str
    round: int
    nbRounds: int
    nbPlayers: int
    nbOngoing: int
    status: str
    rated: bool
    stats: Union[Stats, None]


class SwissResult(TypedDict):
    rank: int
    points: int
    tieBreak: float
    rating: int
    userName: str
    performance: int
