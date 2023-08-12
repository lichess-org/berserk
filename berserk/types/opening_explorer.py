from __future__ import annotations

from typing import cast, Literal
from typing_extensions import TypedDict

OpeningExplorerVariant = Literal[
    "standard",
    "chess960",
    "crazyhouse",
    "antichess",
    "atomic",
    "horde",
    "kingOfTheHill",
    "racingKings",
    "threeCheck",
    "fromPosition",
]

Speed = Literal[
    "ultraBullet", "bullet", "blitz", "rapid", "classical", "correspondence"
]

OpeningExplorerRating = Literal[
    "0", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2500"
]


class Opening(TypedDict):
    # The eco code of this opening
    eco: str
    # The name of this opening
    name: str


class Player(TypedDict):
    # The name of the player
    name: str
    # The rating of the player during the game
    rating: int


class Game(TypedDict):
    # The move in Universal Chess Interface notation
    uci: str
    # The id of the game
    id: str
    # The winner of the game. Draw if None
    winner: Literal["white"] | Literal["black"] | None
    # The speed of the game
    speed: Speed
    # The type of game
    mode: Literal["rated"] | Literal["casual"]
    # The black player
    black: Player
    # The white player
    white: Player
    # The year of the game
    year: int
    # The month and year of the game. For example "2023-06"
    month: str


class Move(TypedDict):
    # The move in Universal Chess Interface notation
    uci: str
    # The move in algebraic notation
    san: str
    # The average rating of games in the position after this move
    averageRating: str # TODO: check why it's `str`, probably wrong
    # The number of white winners after this move
    white: int
    # The number of black winners after this move
    black: int
    # The number of draws after this move
    draws: int
    # The game where the move was played
    game: Game | None


class OpeningStatistic(TypedDict):
    # Number of game won by white from this position
    white: int
    # Number of game won by black from this position
    draws: int
    # Number draws from this position
    black: int
    # Opening info of this position
    opening: Opening | None
    # The list of moves played by players from this position
    moves: list[Move]
    # recent games with this opening
    recentGames: list[Game]
    # top rating games with this opening
    topGames: list[Game]