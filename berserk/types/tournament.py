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


class TournamentInfo(TypedDict):
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
