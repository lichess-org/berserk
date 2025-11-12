from __future__ import annotations

from typing import Iterator, Any, Dict

from .. import models
from ..formats import NDJSON
from .base import BaseClient


class Relations(BaseClient):
    def get_users_followed(self) -> Iterator[Dict[str, Any]]:
        """Stream users you are following.

        :return: iterator over the users the given user follows
        """
        path = "/api/rel/following"
        yield from self._r.get(
            path, stream=True, fmt=NDJSON, converter=models.User.convert
        )

    def follow(self, username: str):
        """Follow a player.

        :param username: user to follow
        """
        path = f"/api/rel/follow/{username}"
        self._r.post(path)

    def unfollow(self, username: str):
        """Unfollow a player.

        :param username: user to unfollow
        """
        path = f"/api/rel/unfollow/{username}"
        self._r.post(path)

    def block(self, username: str):
        """Block a player.

        :param username: user to block
        """
        path = f"/api/rel/block/{username}"
        self._r.post(path)

    def unblock(self, username: str):
        """Unblock a player.

        :param username: user to unblock
        """
        path = f"/api/rel/unblock/{username}"
        self._r.post(path)
