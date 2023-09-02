from __future__ import annotations

from typing import Iterator, cast, List, Literal, TypedDict
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
    # The winner of the game. Draw if None
    winner: Literal["white", "black"] | None
    # The speed of the game
    speed: Speed
    # The type of game
    mode: Literal["rated", "casual"]
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
        play: List[str] | None = None,
        speeds: List[Speed] | None = None,
        ratings: List[OpeningExplorerRating] | None = None,
        since: str | None = None,
        until: str | None = None,
        moves: int | None = None,
        top_games: int | None = None,
        recent_games: int | None = None,
        history: bool | None = None,
    ) -> OpeningStatistic:
        """Get most played move from a position based on lichess games."""

        path = "/lichess"

        if top_games and top_games >= 4:
            logger.warn(
                "The Lichess API caps the top games parameter to 4 (you requested %d)",
                top_games,
            )

        if recent_games and recent_games >= 4:
            logger.warn(
                "The Lichess API caps the recent games parameter to 4 (you requested %d)",
                recent_games,
            )

        params = {
            "variant": variant,
            "fen": position,
            "play": ",".join(play) if play else None,
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

    def get_masters_games(
        self,
        position: str | None = None,
        play: List[str] | None = None,
        since: int | None = None,
        until: int | None = None,
        moves: int | None = None,
        top_games: int | None = None,
    ) -> OpeningStatistic:
        """Get most played move from a position based on masters games."""

        path = "/masters"

        params = {
            "fen": position,
            "play": ",".join(play) if play else None,
            "since": since,
            "until": until,
            "moves": moves,
            "topGames": top_games,
        }
        return cast(OpeningStatistic, self._r.get(path, params=params))

    def get_player_games(
        self,
        player: str,
        color: Literal["white", "black"],
        variant: OpeningExplorerVariant | None = None,
        position: str | None = None,
        play: List[str] | None = None,
        speeds: List[Speed] | None = None,
        ratings: List[OpeningExplorerRating] | None = None,
        since: int | None = None,
        until: int | None = None,
        moves: int | None = None,
        top_games: int | None = None,
        recent_games: int | None = None,
        history: bool | None = None,
        wait_for_indexing: bool = True,
    ) -> OpeningStatistic:
        """Get most played move from a position based on player games.

        The complete statistics for a player may not immediately be available at the
        time of the request. If ``wait_for_indexing`` is true, berserk will wait for
        Lichess to complete indexing the games of the player and return the final
        result. Otherwise, it will return the first result available, which may be empty,
        outdated, or incomplete.

        If you want to get intermediate results during indexing, use ``stream_player_games``.
        """
        iterator = self.stream_player_games(
            player,
            color,
            variant,
            position,
            play,
            speeds,
            ratings,
            since,
            until,
            moves,
            top_games,
            recent_games,
            history,
        )
        result = next(iterator)
        if wait_for_indexing:
            for result in iterator:
                continue
        return result

    def stream_player_games(
        self,
        player: str,
        color: Literal["white", "black"],
        variant: OpeningExplorerVariant | None = None,
        position: str | None = None,
        play: List[str] | None = None,
        speeds: List[Speed] | None = None,
        ratings: List[OpeningExplorerRating] | None = None,
        since: int | None = None,
        until: int | None = None,
        moves: int | None = None,
        top_games: int | None = None,
        recent_games: int | None = None,
        history: bool | None = None,
    ) -> Iterator[OpeningStatistic]:
        """Get most played move from a position based on player games.

        The complete statistics for a player may not immediately be available at the
        time of the request. If it is already available, the returned iterator will
        only have one element with the result, otherwise it will return the last known
        state first and provide updated statistics as games of the player are indexed.
        """

        path = "/player"

        if top_games and top_games >= 4:
            logger.warn(
                "The Lichess API caps the top games parameter to 4 (you requested %d)",
                top_games,
            )

        if recent_games and recent_games >= 4:
            logger.warn(
                "The Lichess API caps the recent games parameter to 4 (you requested %d)",
                recent_games,
            )

        params = {
            "player": player,
            "color": color,
            "variant": variant,
            "fen": position,
            "play": ",".join(play) if play else None,
            "speeds": ",".join(speeds) if speeds else None,
            "ratings": ",".join(ratings) if ratings else None,
            "since": since,
            "until": until,
            "moves": moves,
            "topGames": top_games,
            "recentGames": recent_games,
            "history": history,
        }

        for response in self._r.get(path, params=params, stream=True):
            yield cast(OpeningStatistic, response)
