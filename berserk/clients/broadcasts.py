from __future__ import annotations

from typing import Iterator, Any, Dict, List

from .. import models
from ..formats import PGN
from .base import BaseClient


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def get_official(self, nb: int | None = None) -> Iterator[Dict[str, Any]]:
        """Get the list of incoming, ongoing, and finished official broadcasts. Sorted
        by start date, most recent first.

        :param nb: maximum number of broadcasts to fetch, default is 20
        :return: iterator over broadcast objects
        """
        path = "/api/broadcast"
        params = {"nb": nb}
        yield from self._r.get(path, params=params, stream=True)

    def create(
        self,
        name: str,
        description: str,
        markdown: str | None = None,
        official: bool = False,
    ) -> Dict[str, Any]:
        """Create a new broadcast.

        :param name: name of the broadcast
        :param description: short description
        :param markdown: long description
        :param official: can only be used by Lichess staff accounts
        :return: created tournament info
        """
        path = "/broadcast/new"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get(self, broadcast_id: str, slug: str = "-") -> Dict[str, Any]:
        """Get a broadcast by ID.

        :param broadcast_id: ID of a broadcast
        :param slug: slug for SEO
        :return: broadcast information
        """
        path = f"/broadcast/{slug}/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(
        self,
        broadcast_id: str,
        name: str,
        description: str,
        markdown: str | None = None,
        official: bool = False,
        slug: str = "-",
    ) -> Dict[str, Any]:
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param broadcast_id: ID of a broadcast
        :param name: name of the broadcast
        :param description: short description
        :param markdown: long description
        :param official: can only be used by Lichess staff accounts
        :param slug: slug for SEO
        :return: updated broadcast information
        """
        path = f"/broadcast/{slug}/{broadcast_id}"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_round_id: str, pgn_games: List[str]) -> None:
        """Manually update an existing broadcast by ID.

        :param broadcast_round_id: ID of a broadcast round
        :param pgn_games: one or more games in PGN format
        """
        path = f"/broadcast/round/{broadcast_round_id}/push"
        games = "\n\n".join(g.strip() for g in pgn_games)
        self._r.post(path, data=games)

    def create_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        startsAt: int | None = None,
    ) -> Dict[str, Any]:
        """Create a new broadcast round to relay external games.

        :param broadcast_id: broadcast tournament ID
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games.
        :param startsAt: Timestamp in milliseconds of broadcast round start
        :return: broadcast round info
        """
        path = f"/broadcast/{broadcast_id}/new"
        payload = {"name": name, "syncUrl": syncUrl, "startsAt": startsAt}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round(self, broadcast_id: str) -> Dict[str, Any]:
        """Get information about a broadcast round.

        :param broadcast_id: broadcast round id (8 characters)
        :return: broadcast round info
        """
        path = f"/broadcast/-/-/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        startsAt: int | None = None,
    ) -> Dict[str, Any]:
        """Update information about a broadcast round that you created.

        :param broadcast_id: broadcast round id
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games
        :param startsAt: Timestamp in milliseconds of broadcast start
        :return: updated broadcast information
        """
        path = f"/broadcast/round/{broadcast_id}/edit"
        payload = {"name": name, "syncUrl": syncUrl, "startsAt": startsAt}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round_pgns(self, broadcast_round_id: str) -> Iterator[str]:
        """Get all games of a single round of a broadcast in pgn format.

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
