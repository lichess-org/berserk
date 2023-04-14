# -*- coding: utf-8 -*-
"""Team-related endpoints."""
from __future__ import annotations

from typing import Any, Dict, Iterator

from .. import models
from ..formats import NDJSON
from .base import BaseClient


class Teams(BaseClient):
    """Client for team-related endpoints."""

    def get_members(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :return: users on the given team
        """
        path = f"api/team/{team_id}/users"
        return self._r.get(path, fmt=NDJSON, stream=True, converter=models.User.convert)

    def join(
        self, team_id: str, message: str | None = None, password: str | None = None
    ) -> bool:
        """Join a team.

        :param team_id: ID of a team
        :param message: Optional request message, if the team requires one
        :param password: Optional password, if the team requires one.
        :return: success
        """
        path = f"/team/{team_id}/join"
        payload = {
            "message": message,
            "password": password,
        }
        return self._r.post(path, json=payload)["ok"]

    def leave(self, team_id: str) -> bool:
        """Leave a team.

        :param team_id: ID of a team
        :return: success
        """
        path = f"/team/{team_id}/quit"
        return self._r.post(path)["ok"]

    def kick_member(self, team_id: str, user_id: str) -> bool:
        """Kick a member out of your team.

        :param team_id: ID of a team
        :param user_id: ID of a team member
        :return: success
        """
        path = f"/team/{team_id}/kick/{user_id}"
        return self._r.post(path)["ok"]
