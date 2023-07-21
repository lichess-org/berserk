from __future__ import annotations

from typing import cast, List, Literal, TypedDict
import requests
import logging

from .base import BaseClient

logger = logging.getLogger("berserk.client.opening_explorer")

EXPLORER_URL = "https://explorer.lichess.ovh"

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
    # The winer of the game. Draw if None
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
    averageRating: str
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
    moves: List[Move]
    # recent games with this opening
    recentGames: List[Game]
    # top rating games with this opening
    topGames: List[Game]


class OpeningExplorer(BaseClient):
    """Openings explorer endpoints."""

    def __init__(self, session: requests.Session, explorer_url: str | None = None):
        super().__init__(session, explorer_url or EXPLORER_URL)

    def get_lichess_games(
        self,
        variant: OpeningExplorerVariant = "standard",
        position: str | None = None,
        play: str | None = None,
        speeds: List[Speed] | None = None,
        ratings: List[OpeningExplorerRating] = [],
        since: str | None = None,
        until: str | None = None,
        moves: int | None = None,
        top_games: int | None = None,
        recent_games: int | None = None,
        history: bool | None = None,
    ) -> OpeningStatistic:
        """Get most played move from a position based on lichess games"""

        path = "/lichess"

        if top_games and top_games >= 4:
            logger.debug(
                "The top games parameter {top_games} is higher than 4. The api doesn't allow it and results can differs"
            )

        if recent_games and recent_games >= 4:
            logger.debug(
                "The recent games parameter {recent_games} is higher than 4. The api doesn't allow it and results can differs"
            )

        params = {
            "variant": variant,
            "fen": position,
            "play": play,
            "speeds": ",".join(speeds) if speeds else None,
            "ratings": ",".join(ratings) if ratings else None,
            "since": since,
            "until": until,
            "moves": moves,
            "topGames": top_games,
            "recentGames": recent_games,
            "history": history,
        }
        return cast(OpeningStatistic, self._r.get(path, params=params))
