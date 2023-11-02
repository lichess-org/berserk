from typing import Any, List, Dict, Optional

from .common import Title, LightUser
from typing_extensions import TypedDict, NotRequired


class CurrentTournaments(TypedDict):
    created: List[Dict[str, Any]]
    started: List[Dict[str, Any]]
    finished: List[Dict[str, Any]]


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
    stats: Optional[Stats]


# private, abstract class
class TournamentResult(TypedDict):
    rank: int
    rating: int
    username: str
    title: NotRequired[Title]
    performance: int


class ArenaResult(TournamentResult):
    score: int


class SwissResult(TournamentResult):
    points: float  # can be .5 in case of draw
    tieBreak: float


class PlayerTeamResult(TypedDict):
    user: LightUser
    score: int


class TeamResult(TypedDict):
    rank: int
    id: str
    score: int
    players: List[PlayerTeamResult]


class TeamBattleResult(TypedDict):
    id: str
    teams: List[TeamResult]
