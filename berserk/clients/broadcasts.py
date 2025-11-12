from __future__ import annotations

from typing import Iterator, Any, Dict, List, cast

from .. import models
from ..formats import PGN
from .base import BaseClient

from ..types.broadcast import BroadcastPlayer, BroadcastTop
from ..utils import to_str


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def get_official(
        self, nb: int | None = None, leaderboard: bool | None = None
    ) -> Iterator[Dict[str, Any]]:
        """Get the list of incoming, ongoing, and finished official broadcasts. Sorted
        by start date, most recent first.

        :param nb: maximum number of broadcasts to fetch, default is 20
        :param leaderboard: include the leaderboards, if available
        :return: iterator over broadcast objects
        """
        path = "/api/broadcast"
        params = {"nb": nb, "leaderboard": leaderboard}
        yield from self._r.get(path, params=params, stream=True)

    def create(
        self,
        name: str,
        description: str,
        auto_leaderboard: bool,
        markdown: str | None = None,
        tier: int | None = None,
        players: List[BroadcastPlayer] | None = None,
    ) -> Dict[str, Any]:
        """Create a new broadcast.

        :param name: name of the broadcast
        :param description: short description
        :param auto_leaderboard: simple leaderboard based on game results
        :param markdown: long description
        :param tier: can only be used by Lichess staff accounts:
            3 for normal, 4 for high, 5 for best
        :param players: replace player names, ratings and titles.
            One line per player, formatted as such:
            Original name; Replacement name; Optional rating; Optional title
        :return: created tournament info
        """
        path = "/broadcast/new"
        payload = {
            "name": name,
            "description": description,
            "autoLeaderboard": auto_leaderboard,
            "markdown": markdown,
            "tier": tier,
            "players": to_str(players),
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get(self, broadcast_id: str) -> Dict[str, Any]:
        """Get a broadcast by ID.

        :param broadcast_id: ID of a broadcast
        :param slug: slug for SEO
        :return: broadcast information
        """
        path = f"api/broadcast/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(
        self,
        broadcast_id: str,
        name: str,
        description: str,
        auto_leaderboard: bool,
        markdown: str | None = None,
        tier: int | None = None,
        players: List[BroadcastPlayer] | None = None,
    ) -> Dict[str, Any]:
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param broadcast_id: ID of a broadcast
        :param name: name of the broadcast
        :param description: short description
        :param auto_leaderboard: simple leaderboard based on game results
        :param markdown: long description
        :param tier: can only be used by Lichess staff accounts:
            3 for normal, 4 for high, 5 for best
        :param players: replace player names, ratings and titles.
            One line per player, formatted as such:
            Original name; Replacement name; Optional rating; Optional title
        :return: updated broadcast information
        """
        path = f"/broadcast/{broadcast_id}/edit"
        payload = {
            "name": name,
            "description": description,
            "autoLeaderboard": auto_leaderboard,
            "markdown": markdown,
            "tier": tier,
            "players": to_str(players),
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_round_id: str, pgn_games: List[str]) -> None:
        """Manually update an existing broadcast by ID.

        :param broadcast_round_id: ID of a broadcast round
        :param pgn_games: one or more games in PGN format
        """
        path = f"/api/broadcast/round/{broadcast_round_id}/push"
        games = "\n\n".join(g.strip() for g in pgn_games)
        self._r.post(path, data=games)

    def create_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        syncUrlRound: str | None = None,
        startsAt: int | None = None,
        delay: int | None = None,
        period: int | None = None,
        finished: bool | None = None,
    ) -> Dict[str, Any]:
        """Create a new broadcast round to relay external games.

        :param broadcast_id: broadcast tournament ID
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games
        :param syncUrlRound: required if syncUrl contains a LiveChessCloud link
        :param startsAt: Timestamp in milliseconds of broadcast round start
        :param delay: how long to delay moves coming from the source in seconds
        :param period: how long to wait between source requests in seconds
        :param finished: set whether the round is completed
        :return: broadcast round info
        """
        path = f"/broadcast/{broadcast_id}/new"
        payload = {
            "name": name,
            "syncUrl": syncUrl,
            "syncUrlRound": syncUrlRound,
            "startsAt": startsAt,
            "delay": delay,
            "period": period,
            "finished": finished,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round(self, broadcast_id: str) -> Dict[str, Any]:
        """Get information about a broadcast round.

        :param broadcast_id: broadcast round ID (8 characters)
        :return: broadcast round info
        """
        path = f"/broadcast/-/-/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        syncUrlRound: str | None = None,
        startsAt: int | None = None,
        delay: int | None = None,
        status: str | None = None,
        period: int | None = None,
    ) -> Dict[str, Any]:
        """Update information about a broadcast round that you created.

        :param broadcast_id: broadcast round ID
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games
        :param syncUrlRound: required if syncUrl contains a LiveChessCloud link
        :param startsAt: Timestamp in milliseconds of broadcast round start
        :param delay: how long to delay moves coming from the source in seconds
        :param status: manual broadcast round status "new", "started" or "finished"
        :param period: how long to wait between source requests in seconds
        :return: updated broadcast information
        """
        path = f"/broadcast/round/{broadcast_id}/edit"
        payload = {
            "name": name,
            "syncUrl": syncUrl,
            "syncUrlRound": syncUrlRound,
            "startsAt": startsAt,
            "delay": delay,
            "status": status,
            "period": period,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round_pgns(self, broadcast_round_id: str) -> Iterator[str]:
        """Get all games of a single round of a broadcast in PGN format.

        :param broadcast_round_id: broadcast round ID
        :return: iterator over all games of the broadcast round in PGN format
        """
        path = f"/api/broadcast/round/{broadcast_round_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)

    def get_pgns(self, broadcast_id: str) -> Iterator[str]:
        """Get all games of all rounds of a broadcast in PGN format.

        :param broadcast_id: the broadcast ID
        :return: iterator over all games of the broadcast in PGN format
        """
        path = f"/api/broadcast/{broadcast_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)

    def stream_round(self, broadcast_round_id: str) -> Iterator[str]:
        """Stream an ongoing broadcast tournament in PGN format.

        This streaming endpoint first sends all games of a broadcast tournament in PGN format.

        Then, it waits for new moves to be played. As soon as it happens, the entire PGN of the game is sent to the stream.

        The stream will also send PGNs when games are added to the tournament.

        :param broadcast_round_id: broadcast round ID
        :return: stream of games of the broadcast round in PGN format
        """
        path = f"/api/stream/broadcast/round/{broadcast_round_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)

    def stream_my_rounds(self, nb: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream all broadcast rounds you are a member of.

        Also includes broadcasts rounds where you're a non-writing member. See the writeable flag in the response.

        Rounds are ordered by rank, which is roughly chronological, most recent first, slightly pondered with popularity.

        :param nb: how many rounds to get
        :return: iterator over broadcast objects with rounds you're a member of and a study.writeable flag
        """
        path = "/api/broadcast/my-rounds"
        params = {"nb": nb}
        yield from self._r.get(path, params=params, stream=True)

    def get_top(
        self,
        page: int = 1,
        html: bool = False,
    ) -> BroadcastTop:
        """Return the paginated top broadcasts structure for `page`.

        :param page: which page to fetch (1..20). Only page 1 has `active` broadcasts.
        :param html: if True, convert the `description` field from markdown to HTML.
        :return: parsed JSON response with keys `active` and `past`.
        """
        path = "/api/broadcast/top"
        params = {"page": page, "html": html}
        return cast(BroadcastTop, self._r.get(path, params=params))
