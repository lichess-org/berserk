# -*- coding: utf-8 -*-
"""TV-related endpoints."""
from .. import models
from ..formats import NDJSON, PGN
from .base import FmtClient


class TV(FmtClient):
    """Client for TV related endpoints."""

    def get_current_games(self):
        """Get basic information about the current TV games being played

        :return: best ongoing games in each speed and variant
        :rtype: dict
        """
        path = "api/tv/channels"
        return self._r.get(path)

    def stream_current_game(self):
        """Streams the current TV game

        :return: positions and moves of the current TV game
        :rtype: dict
        """
        path = "api/tv/feed"
        yield from self._r.get(path, stream=True)

    def get_best_ongoing(
        self,
        channel,
        as_pgn=None,
        count=None,
        moves=None,
        pgn_in_json=None,
        tags=None,
        clocks=None,
        opening=None,
    ):
        """Get a list of ongoing games for a given TV channel in PGN or NDJSON.

        :param str channel: the name of the TV channel in camel case
        :param bool as_pgn: whether to return the game in PGN format
        :param int count: the number of games to fetch [1..30]
        :param bool moves: whether to include the PGN moves
        :param bool pgn_in_json: include the full PGN within JSON response
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves
        :param bool opening: whether to include the opening name
        :return: the ongoing games of the given TV channel in PGN or NDJSON
        """
        path = f"api/tv/{channel}"
        params = {
            "nb": count,
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.TV.convert
            )
