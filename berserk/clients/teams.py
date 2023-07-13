from __future__ import annotations

from typing import Iterator, Any, Dict

from .. import models
from ..formats import NDJSON, JSON_LIST
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

    def get_join_requests(
        self, team_id: str, declined: bool = False
    ) -> list[Dict[str, Any]]:
        """Get pending join requests of your team

        :param team_id: ID of a team
        :param declined: Get the declined join requests
        :return: List of join requests
        """
        path = f"/api/team/{team_id}/requests"
        params = {"declined": declined}
        return self._r.get(path, params=params, fmt=JSON_LIST)

    def accept_join_request(self, team_id: str, user_id: str) -> None:
        """Accept someone's request to join the team

        :param team_id: ID of a team
        :param user_id: ID of a member requesting to join
        """
        path = f"/api/team/{team_id}/request/{user_id}/accept"
        self._r.post(path)
