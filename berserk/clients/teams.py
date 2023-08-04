from __future__ import annotations

from typing import Iterator, Any, Dict, List, Literal, TypedDict, cast

from .. import models
from ..formats import NDJSON, JSON_LIST
from .base import BaseClient

Title = Literal[
    "GM", "WGM", "IM", "WIM", "FM", "WFM", "NM", "CM", "WCM", "WNM", "LM", "BOT"
]


class Team(TypedDict):
    # The id of the team
    id: str
    # The name of the team
    name: str
    # The description of the team
    description: str
    # Whether the team is open
    open: bool
    # The leader of the team
    leader: LightUser
    # The leaders of the team
    leaders: List[LightUser]
    # The number of members of the team
    nbMembers: int
    # Has the user asssociated with the token (if any) joined the team
    joined: bool
    # Has the user asssociated with the token (if any) requested to join the team
    requested: bool


class LightUser(TypedDict):
    # The id of the user
    id: str
    # The name of the user
    name: str
    # The title of the user
    title: Title
    # The patron of the user
    patron: bool


class Teams(BaseClient):
    def get_members(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :param team_id: ID of the team to get members from
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

        :param team_id: ID of the team to join
        :param message: optional request message, if the team requires one
        :param password: optional password, if the team requires one
        """
        path = f"/team/{team_id}/join"
        payload = {
            "message": message,
            "password": password,
        }
        self._r.post(path, json=payload)

    def leave(self, team_id: str) -> None:
        """Leave a team.

        :param team_id: ID of the team to leave
        """
        path = f"/team/{team_id}/quit"
        self._r.post(path)

    def kick_member(self, team_id: str, user_id: str) -> None:
        """Kick a member out of your team.

        :param team_id: ID of the team to kick from
        :param user_id: ID of the user to kick from the team
        """
        path = f"/team/{team_id}/kick/{user_id}"
        self._r.post(path)

    def get_join_requests(
        self, team_id: str, declined: bool = False
    ) -> List[Dict[str, Any]]:
        """Get pending join requests of your team

        :param team_id: ID of the team to request the join requests from
        :param declined: whether to show declined requests instead of pending ones
        :return: list of join requests
        """
        path = f"/api/team/{team_id}/requests"
        params = {"declined": declined}
        return self._r.get(path, params=params, fmt=JSON_LIST)

    def accept_join_request(self, team_id: str, user_id: str) -> None:
        """Accept someone's request to join one of your teams

        :param team_id: ID of the team to accept the request for
        :param user_id: ID of the user requesting to join
        """
        path = f"/api/team/{team_id}/request/{user_id}/accept"
        self._r.post(path)

    def get_team(self, team_id: str) -> Team:
        """Get the information about the team

        :return: the information about the team
        """
        path = f"/api/team/{team_id}"
        return cast(Team, self._r.get(path))

    def teams_of_player(self, username: str) -> List[Team]:
        """Get all the teams a player is a member of

        :return: list of teams the user is a member of
        """
        path = f"/api/team/of/{username}"
        return cast(List[Team], self._r.get(path))
