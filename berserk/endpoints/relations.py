# -*- coding: utf-8 -*-
"""Relations-related endpoints."""
from typing import Any, Dict, Iterator

from .. import models
from ..formats import NDJSON
from . import BaseClient


class Relations(BaseClient):
    """Client for relations-related endpoints."""

    def get_users_followed(self) -> Iterator[Dict[str, Any]]:
        """Stream users you are following.

        :return: iterator over the users the given user follows
        """
        path = "/api/rel/following"
        return self._r.get(path, stream=True, fmt=NDJSON, converter=models.User.convert)

    def follow(self, username: str) -> bool:
        """Follow a player.

        :param username: user to follow
        :return: success
        """
        path = f"/api/rel/follow/{username}"
        return self._r.post(path)["ok"]

    def unfollow(self, username: str) -> bool:
        """Unfollow a player.

        :param username: user to unfollow
        :return: success
        """
        path = f"/api/rel/unfollow/{username}"
        return self._r.post(path)["ok"]
