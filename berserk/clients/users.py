from __future__ import annotations

from typing import Iterator, Dict, List, Any
from deprecated import deprecated

from .. import models
from .base import BaseClient
from ..formats import JSON_LIST, LIJSON, NDJSON
from ..types.common import PerfType
from ..session import Params


class Users(BaseClient):
    """Client for user-related endpoints."""

    @deprecated(reason="Use Puzzles.get_puzzle_activity instead", version="0.12.6")
    def get_puzzle_activity(self, max: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history of the authenticated user, starting with the
        most recent activity.

        :param max: maximum number of entries to stream. defaults to all activity
        :return: stream of puzzle activity history
        """
        path = "/api/puzzle/activity"
        params = {"max": max}
        yield from self._r.get(
            path,
            params=params,
            fmt=NDJSON,
            stream=True,
            converter=models.PuzzleActivity.convert,
        )

    def get_realtime_statuses(
        self, *user_ids: str, with_game_ids: bool = False
    ) -> List[Dict[str, Any]]:
        """Get the online, playing, and streaming statuses of players.

        Only id and name fields are returned for offline users.

        :param user_ids: one or more user IDs (names)
        :param with_game_ids: whether or not to return IDs of the games being played
        :return: statuses of given players
        """
        path = "/api/users/status"
        params: Params = {"ids": ",".join(user_ids), "withGameIds": with_game_ids}

        return self._r.get(path, fmt=JSON_LIST, params=params)

    def get_all_top_10(self) -> Dict[str, Any]:
        """Get the top 10 players for each speed and variant.

        :return: top 10 players in each speed and variant
        """
        path = "/api/player"
        return self._r.get(path, fmt=LIJSON)

    def get_player_by_autocomplete(
        self, partial_username: str, object: bool = False
    ) -> List[str] | Dict[str, Any]:
        """Provides autocompletion options for an incomplete username.

        :param partial_username: the beginning of a username, must provide >= 3 characters
        :param object: if false, returns an array of usernames else if true, returns an object with matching users
        :return: followed players matching term if any, else returns other players. Requires OAuth.
        """
        path = "/api/player/autocomplete"
        params: Params = {"partial_username": partial_username, "object": object}

        return self._r.get(path, fmt=LIJSON, params=params)

    def get_leaderboard(self, perf_type: PerfType, count: int = 10):
        """Get the leaderboard for one speed or variant.

        :param perf_type: speed or variant
        :param count: number of players to get
        :return: top players for one speed or variant
        """
        path = f"/api/player/top/{count}/{perf_type}"
        return self._r.get(path, fmt=LIJSON)["users"]

    def get_public_data(self, username: str) -> Dict[str, Any]:
        """Get the public data for a user.

        :return: public data available for the given user
        """
        path = f"/api/user/{username}"
        return self._r.get(path, converter=models.User.convert)

    def get_activity_feed(self, username: str) -> List[Dict[str, Any]]:
        """Get the activity feed of a user.

        :return: activity feed of the given user
        """
        path = f"/api/user/{username}/activity"
        return self._r.get(path, fmt=JSON_LIST, converter=models.Activity.convert)

    def get_by_id(self, *usernames: str) -> List[Dict[str, Any]]:
        """Get multiple users by their IDs.

        :param usernames: one or more usernames
        :return: user data for the given usernames
        """
        path = "/api/users"
        return self._r.post(
            path, data=",".join(usernames), fmt=JSON_LIST, converter=models.User.convert
        )

    def get_live_streamers(self) -> List[Dict[str, Any]]:
        """Get basic information about currently streaming users.

        :return: users currently streaming a game
        """
        path = "/api/streamer/live"
        return self._r.get(path, fmt=JSON_LIST)

    def get_rating_history(self, username: str) -> List[Dict[str, Any]]:
        """Get the rating history of a user.

        :return: rating history for all game types
        """
        path = f"/api/user/{username}/rating-history"
        return self._r.get(path, fmt=JSON_LIST, converter=models.RatingHistory.convert)

    def get_crosstable(
        self, user1: str, user2: str, matchup: bool = False
    ) -> List[Dict[str, Any]]:
        """Get total number of games, and current score, of any two users.

        :param user1: first user to compare
        :param user2: second user to compare
        :param matchup: Whether to get the current match data, if any
        """
        params = {"matchup": matchup}
        path = f"/api/crosstable/{user1}/{user2}"
        return self._r.get(
            path, params=params, fmt=JSON_LIST, converter=models.User.convert
        )

    def get_user_performance(self, username: str, perf: str) -> List[Dict[str, Any]]:
        """Read performance statistics of a user, for a single performance.

        Similar to the performance pages on the website
        """
        path = f"/api/user/{username}/perf/{perf}"
        return self._r.get(path, fmt=JSON_LIST, converter=models.User.convert)
