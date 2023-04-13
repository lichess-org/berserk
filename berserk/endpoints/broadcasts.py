# -*- coding: utf-8 -*-
"""Broadcasts-related endpoints."""
from .. import models
from .base import BaseClient


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def create(self, name, description, markdown=None, official=None):
        """Create a new broadcast.

        :param str name: name of the broadcast
        :param str description: short description
        :param str markdown: long description
        :param bool official: DO NOT USE
        :return: created tournament info
        :rtype: dict
        """
        path = "broadcast/new"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get(self, broadcast_id, slug="-"):
        """Get a broadcast by ID.

        :param str broadcast_id: ID of a broadcast
        :param str slug: slug for SEO
        :return: broadcast information
        :rtype: dict
        """
        path = f"broadcast/{slug}/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(
        self, broadcast_id, name, description, markdown=None, official=None, slug="-"
    ):
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param str broadcast_id: ID of a broadcast
        :param str name: name of the broadcast
        :param str description: short description
        :param str markdown: long description
        :param bool official: DO NOT USE
        :param str slug: slug for SEO
        :return: updated broadcast information
        :rtype: dict
        """
        path = f"broadcast/{slug}/{broadcast_id}"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_round_id, pgn_games):
        """Manually update an existing broadcast by ID.

        :param str broadcast_round_id: ID of a broadcast round
        :param list pgn_games: one or more games in PGN format
        :return: success
        :rtype: bool
        """
        path = f"broadcast/round/{broadcast_round_id}/push"
        games = "\n\n".join(g.strip() for g in pgn_games)
        return self._r.post(path, data=games)["ok"]

    def create_round(self, broadcast_id, name, sync_url=None, starts_at=None):
        """Create a new broadcast round to relay external games.

        :param str broadcast_id: broadcast tournament ID
        :param str name: Name of the broadcast round
        :param str sync_url: URL that Lichess will poll to get updates about the games.
        :param int starts_at: Timestamp in milliseconds of broadcast round start
        :return: success
        :rtype: dict
        """
        path = f"broadcast/{broadcast_id}/new"
        payload = {"name": name, "syncUrl": sync_url, "startsAt": starts_at}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round(
        self, broadcast_id, broadcast_tournament_slug="-", broadcast_round_slug="-"
    ):
        """Get information about a broadcast round

        :param broadcast_id: broadcast round id
        :param str broadcast_tournament_slug: Only used for SEO, can be safely replaced by -
        :param str broadcast_round_slug: Only used for SEO, can be safely replaced by -
        :return: broadcast round info
        :rtype: dict
        """
        path = (
            f"broadcast/{broadcast_tournament_slug}/{broadcast_round_slug}"
            + f"/{broadcast_id}"
        )
        return self._r.get(path, converter=models.Broadcast.convert)

    def update_round(self, broadcast_id, name, sync_url=None, starts_at=None):
        """Update information about a broadcast round that you created

        :param str broadcast_id: broadcast round id
        :param str name: Name of the broadcast round
        :param str sync_url: URL that Lichess will poll to get updates about the games
        :param starts_at: Timestamp in milliseconds of broadcast start
        :return: updated broadcast information
        :rtype: dict
        """
        path = f"broadcast/round/{broadcast_id}/edit"
        payload = {"name": name, "syncUrl": sync_url, "startsAt": starts_at}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)
