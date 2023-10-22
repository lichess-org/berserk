from __future__ import annotations

from typing import Iterator, cast
import requests
import logging

from .base import BaseClient
from ..types import (
    OpeningStatistic,
    OpeningExplorerVariant,
    Speed,
    OpeningExplorerRating,
)
from ..types.common import Color

logger = logging.getLogger("berserk.client.opening_explorer")

EXPLORER_URL = "https://explorer.lichess.ovh"


class OpeningExplorer(BaseClient):
    """Openings explorer endpoints."""

    def __init__(self, session: requests.Session, explorer_url: str | None = None):
        super().__init__(session, explorer_url or EXPLORER_URL)

    def get_lichess_games(
        self,
        variant: OpeningExplorerVariant = "standard",
        position: str | None = None,
        play: list[str] | None = None,
        speeds: list[Speed] | None = None,
        ratings: list[OpeningExplorerRating] | None = None,
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
        play: list[str] | None = None,
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
        color: Color,
        variant: OpeningExplorerVariant | None = None,
        position: str | None = None,
        play: list[str] | None = None,
        speeds: list[Speed] | None = None,
        ratings: list[OpeningExplorerRating] | None = None,
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
        color: Color,
        variant: OpeningExplorerVariant | None = None,
        position: str | None = None,
        play: list[str] | None = None,
        speeds: list[Speed] | None = None,
        ratings: list[OpeningExplorerRating] | None = None,
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

    def get_otb_master_game(self, game_id: str):
        """Get PGN representation of an over-the-board master game.

        :param game_id: game ID
        :return: PGN of the game
        """
        path = f"/master/pgn/{game_id}"
        return self._r.get(path)
