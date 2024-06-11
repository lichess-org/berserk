from __future__ import annotations

from typing import Any, Iterator, Dict, List, cast

from .. import models
from ..formats import NDJSON_LIST, PGN
from ..types import TVFeed
from .base import FmtClient


class TV(FmtClient):
    """Client for TV related endpoints."""

    def get_current_games(self) -> Dict[str, Any]:
        """Get basic information about the current TV games being played.

        :return: best ongoing games in each speed and variant
        """
        path = "/api/tv/channels"
        return self._r.get(path)

    def stream_current_game(self) -> Iterator[TVFeed]:
        """Streams the current TV game.

        :return: positions and moves of the current TV game
        """
        path = "/api/tv/feed"
        for response in self._r.get(path, stream=True):
            yield cast(TVFeed, response)

    def stream_current_game_of_channel(self, channel: str) -> Iterator[TVFeed]:
        """Streams the current TV game of a channel.

        :param channel: the TV channel to stream.
        :return: positions and moves of the channels current TV game
        """
        path = f"/api/tv/{channel}/feed"
        for response in self._r.get(path, stream=True):
            yield cast(TVFeed, response)

    def get_best_ongoing(
        self,
        channel: str,
        as_pgn: bool | None = None,
        count: int | None = None,
        moves: bool = True,
        pgnInJson: bool = False,
        tags: bool = True,
        clocks: bool = False,
        opening: bool = False,
    ) -> str | List[Dict[str, Any]]:
        """Get a list of ongoing games for a given TV channel in PGN or NDJSON.

        :param channel: the name of the TV channel in camel case
        :param as_pgn: whether to return the game in PGN format
        :param count: the number of games to fetch [1..30]
        :param moves: whether to include the PGN moves
        :param pgnInJson: include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param opening: whether to include the opening name
        :return: the ongoing games of the given TV channel in PGN or NDJSON
        """
        path = f"/api/tv/{channel}"
        params = {
            "nb": count,
            "moves": moves,
            "pgnInJson": pgnInJson,
            "tags": tags,
            "clocks": clocks,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON_LIST, converter=models.TV.convert
            )
