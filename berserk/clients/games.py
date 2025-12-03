from __future__ import annotations

from typing import Iterator, Any, Dict, List

from .. import models
from ..formats import PGN, NDJSON
from ..types.common import Color, PerfType
from .base import FmtClient


class Games(FmtClient):
    """Client for games-related endpoints."""

    def export(
        self,
        game_id: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        pgn_in_json: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        literate: bool | None = None,
    ) -> str | Dict[str, Any]:
        """Get one finished game as PGN or JSON.

        :param game_id: the ID of the game to export
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param pgn_in_json: include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :return: exported game, as JSON or PGN
        """
        path = f"/game/export/{game_id}"
        params = {
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "literate": literate,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(path, params=params, converter=models.Game.convert)

    def export_ongoing_by_player(
        self,
        username: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        pgn_in_json: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        literate: bool | None = None,
        players: str | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Export the ongoing game, or the last game played, of a user.

        :param username: the player's username
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param pgn_in_json: include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :param players: URL of text file containing real names and ratings for PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/user/{username}/current-game"
        params = {
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "literate": literate,
            "players": players,
        }
        if self._use_pgn(as_pgn):
            yield from self._r.get(path, params=params, stream=True, fmt=PGN)
        else:
            yield from self._r.get(
                path,
                params=params,
                stream=True,
                converter=models.Game.convert,
            )

    def export_by_player(
        self,
        username: str,
        as_pgn: bool | None = None,
        since: int | None = None,
        until: int | None = None,
        max: int | None = None,
        vs: str | None = None,
        rated: bool | None = None,
        perf_type: PerfType | None = None,
        color: Color | None = None,
        analysed: bool | None = None,
        moves: bool | None = None,
        pgn_in_json: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        ongoing: bool | None = None,
        finished: bool | None = None,
        players: str | None = None,
        sort: str | None = None,
        literate: bool | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Get games by player.

        :param username: which player's games to return
        :param as_pgn: whether to return the game in PGN format
        :param since: lower bound on the game timestamp
        :param until: upperbound on the game timestamp
        :param max: limit the number of games returned
        :param vs: filter by username of the opponent
        :param rated: filter by game mode (``True`` for rated, ``False`` for casual)
        :param perf_type: filter by speed or variant
        :param color: filter by the color of the player
        :param analysed: filter by analysis availability
        :param moves: whether to include the PGN moves
        :param pgn_in_json: Include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param ongoing: Include ongoing games, last 3 moves omitted
        :param finished: Include finished games
        :param players: URL of text file containing real names and ratings for PGN
        :param sort: Sort the order of games
        :param literate: whether to include literate the PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/games/user/{username}"
        params = {
            "since": since,
            "until": until,
            "max": max,
            "vs": vs,
            "rated": rated,
            "perfType": perf_type,
            "color": color,
            "analysed": analysed,
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "ongoing": ongoing,
            "finished": finished,
            "players": players,
            "sort": sort,
            "literate": literate,
        }
        if self._use_pgn(as_pgn):
            yield from self._r.get(path, params=params, fmt=PGN, stream=True)
        else:
            yield from self._r.get(
                path,
                params=params,
                fmt=NDJSON,
                stream=True,
                converter=models.Game.convert,
            )

    def export_multi(
        self,
        *game_ids: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Get multiple games by ID.

        :param game_ids: one or more game IDs to export
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
        path = "/api/games/export/_ids"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        payload = ",".join(game_ids)
        if self._use_pgn(as_pgn):
            yield from self._r.post(
                path,
                params=params,
                data=payload,
                fmt=PGN,
                stream=True,
            )
        else:
            yield from self._r.post(
                path,
                params=params,
                data=payload,
                fmt=NDJSON,
                stream=True,
                converter=models.Game.convert,
            )

    def get_among_players(
        self, *usernames: str, with_current_games: bool = False
    ) -> Iterator[Dict[str, Any]]:
        """Stream the games currently being played among players.

        Note this will not include games where only one player is in the given list of
        usernames. The stream will emit an event each time a game is started or
        finished.

        :param usernames: two or more usernames
        :param with_current_games: include all current ongoing games at the beginning of
            the stream
        :return: iterator over all games played among the given players
        """
        path = "/api/stream/games-by-users"
        params = {
            "withCurrentGames": with_current_games,
        }
        payload = ",".join(usernames)
        yield from self._r.post(
            path,
            params=params,
            data=payload,
            fmt=NDJSON,
            stream=True,
            converter=models.Game.convert,
        )

    def stream_games_by_ids(
        self, *game_ids: str, stream_id: str
    ) -> Iterator[Dict[str, Any]]:
        """Stream multiple games by ID.

        :param game_ids: one or more game IDs to stream
        :param stream_id: arbitrary stream ID that can be used later to add game IDs to
            this stream
        :return: iterator over the stream of results
        """
        path = f"/api/stream/games/{stream_id}"
        payload = ",".join(game_ids)
        yield from self._r.post(
            path, data=payload, fmt=NDJSON, stream=True, converter=models.Game.convert
        )

    def add_game_ids_to_stream(self, *game_ids: str, stream_id: str) -> None:
        """Add new game IDs to an existing stream.

        :param stream_id: the stream ID you used to create the existing stream
        :param game_ids: one or more game IDs to stream
        """
        path = f"/api/stream/games/{stream_id}/add"
        payload = ",".join(game_ids)
        self._r.post(path, data=payload)

    def get_ongoing(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get your currently ongoing games.

        :param count: number of games to get
        :return: some number of currently ongoing games
        """
        path = "/api/account/playing"
        params = {"nb": count}
        return self._r.get(path, params=params)["nowPlaying"]

    def stream_game_moves(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Stream positions and moves of any ongoing game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"/api/stream/game/{game_id}"
        yield from self._r.get(path, stream=True)

    def import_game(self, pgn: str) -> Dict[str, Any]:
        """Import a single game from PGN.

        :param pgn: the PGN of the game
        :return: the game ID and URL of the import
        """
        path = "/api/import"
        payload = {
            "pgn": pgn,
        }
        return self._r.post(path, data=payload)

    def export_imported(self) -> str:
        """
        Export all the imported games by the currently logged in user
        as a PGN.
        Requires OAuth2 authorization.

        :return: the exported games in a single string
        """
        path = "/api/games/export/imports"
        return self._r.get(path, fmt=PGN, stream=False)
