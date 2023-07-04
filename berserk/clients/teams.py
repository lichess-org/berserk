from __future__ import annotations

from typing import Iterator, Any, Dict

from .. import models
from ..formats import NDJSON
from .base import BaseClient


class Teams(BaseClient):
    def get_members(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :return: users on the given team
        """
        path = f"/api/team/{team_id}/users"
        yield from self._r.get(
            path, fmt=NDJSON, stream=True, converter=models.User.convert
        )

    def join(
        self, team_id: str, message: str | None = None, password: str | None = None
    ) -> None:
        """Join a team.

        :param team_id: ID of a team
        :param message: Optional request message, if the team requires one
        :param password: Optional password, if the team requires one.
        """
        path = f"/team/{team_id}/join"
        payload = {
            "message": message,
            "password": password,
        }
        self._r.post(path, json=payload)

    def leave(self, team_id: str) -> None:
        """Leave a team.

        :param team_id: ID of a team
        """
        path = f"/team/{team_id}/quit"
        self._r.post(path)

    def kick_member(self, team_id: str, user_id: str) -> None:
        """Kick a member out of your team.

        :param team_id: ID of a team
        :param user_id: ID of a team member
        """
        path = f"/team/{team_id}/kick/{user_id}"
        self._r.post(path)
