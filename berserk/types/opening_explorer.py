from __future__ import annotations

from typing import Generic, Literal, List, TypeVar
from typing_extensions import TypedDict, NotRequired
from .common import Color, Speed

OpeningExplorerRating = Literal[
    "0", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2500"
]


MoveT = TypeVar("MoveT")
GameT = TypeVar("GameT")


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


class GameWithoutUci(TypedDict):
    # The id of the game
    id: str
    # The winner of the game. Draw if None
    winner: Color | None
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


class MastersGameWithoutUci(TypedDict):
    # The id of the OTB master game
    id: str
    # The winner of the game. Draw if None
    winner: Color | None
    # The black player
    black: Player
    # The white player
    white: Player
    # The year of the game
    year: int
    # The month and year of the game. For example "2023-06"
    month: NotRequired[str]


class Game(GameWithoutUci):
    # The move in Universal Chess Interface notation
    uci: str


class MastersGame(MastersGameWithoutUci):
    # The move in Universal Chess Interface notation
    uci: str


class Move(TypedDict):
    # The move in Universal Chess Interface notation
    uci: str
    # The move in algebraic notation
    san: str
    # The average rating of games in the position after this move
    averageRating: int
    # The number of white winners after this move
    white: int
    # The number of black winners after this move
    black: int
    # The number of draws after this move
    draws: int
    # The game where the move was played
    game: GameWithoutUci | None
    # The opening info for this move
    opening: Opening | None


class PlayerMove(TypedDict):
    # The move in Universal Chess Interface notation
    uci: str
    # The move in algebraic notation
    san: str
    # The average opponent rating in games with this move
    averageOpponentRating: int
    # The performance rating for this move
    performance: int
    # The number of white winners after this move
    white: int
    # The number of black winners after this move
    black: int
    # The number of draws after this move
    draws: int
    # The game where the move was played
    game: GameWithoutUci | None
    # The opening info for this move
    opening: Opening | None


class MastersMove(TypedDict):
    # The move in Universal Chess Interface notation
    uci: str
    # The move in algebraic notation
    san: str
    # The average rating of games in the position after this move
    averageRating: int
    # The number of white winners after this move
    white: int
    # The number of black winners after this move
    black: int
    # The number of draws after this move
    draws: int
    # The OTB master game where the move was played
    game: MastersGameWithoutUci | None
    # The opening info for this move
    opening: Opening | None


class BaseOpeningStatistic(TypedDict, Generic[MoveT, GameT]):
    # Number of game won by white from this position
    white: int
    # Number of game won by black from this position
    draws: int
    # Number draws from this position
    black: int
    # Opening info of this position
    opening: Opening | None
    # The list of moves played from this position
    moves: List[MoveT]


class OpeningStatistic(BaseOpeningStatistic[Move, Game]):
    # top rating games with this opening
    topGames: List[Game]
    # recent games with this opening (optional per schema)
    recentGames: NotRequired[List[Game]]


class PlayerOpeningStatistic(BaseOpeningStatistic[PlayerMove, Game]):
    # Queue position for indexing (present when wait_for_indexing parameter used)
    queuePosition: int
    # recent games with this opening
    recentGames: List[Game]


class MastersOpeningStatistic(BaseOpeningStatistic[MastersMove, MastersGame]):
    # top rating OTB master games with this opening
    topGames: List[MastersGame]
