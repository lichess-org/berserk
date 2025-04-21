from __future__ import annotations

from typing import Iterator, Any, Dict, cast

from .. import models
from ..formats import NDJSON
from .base import BaseClient
from ..types import PuzzleRace, NextPuzzle


class Puzzles(BaseClient):
    """Client for puzzle-related endpoints."""

    def get_daily(self) -> Dict[str, Any]:
        """Get the current daily Lichess puzzle.

        :return: current daily puzzle
        """
        path = "/api/puzzle/daily"
        return self._r.get(path)

    def get(self, id: str) -> Dict[str, Any]:
        """Get a puzzle by its id.

        :param id: the id of the puzzle to retrieve
        :return: the puzzle
        """
        path = f"/api/puzzle/{id}"
        return self._r.get(path)

    def get_puzzle_activity(
        self, max: int | None = None, before: int | None = None
    ) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history of the authenticated user, starting with the
        most recent activity.

        :param max: maximum number of entries to stream. defaults to all activity
        :param before: timestamp in milliseconds. only stream activity before this time.
            defaults to now. use together with max for pagination
        :return: iterator over puzzle activity history
        """
        path = "/api/puzzle/activity"
        params = {"max": max, "before": before}
        yield from self._r.get(
            path,
            params=params,
            fmt=NDJSON,
            stream=True,
            converter=models.PuzzleActivity.convert,
        )

    def get_puzzle_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """Get the puzzle dashboard of the authenticated user.

        :param days: how many days to look back when aggregating puzzle results
        :return: the puzzle dashboard
        """
        path = f"/api/puzzle/dashboard/{days}"
        return self._r.get(path)

    def get_storm_dashboard(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get storm dashboard of a player. Set days to 0 if you're only interested in
        the high score.

        :param username: the username of the player to download the dashboard for
        :param days: how many days of history to return
        :return: the storm dashboard
        """
        path = f"/api/storm/dashboard/{username}"
        params = {"days": days}
        return self._r.get(path, params=params)

    def create_race(self) -> PuzzleRace:
        """Create a new private puzzle race. The Lichess user who creates the race must join the race page,
        and manually start the race when enough players have joined.

        :return: puzzle race ID and URL
        """
        path = "/api/racer"
        return cast(PuzzleRace, self._r.post(path))

    def get_next_puzzle(self, rating: int | None = None) -> NextPuzzle:
        """Get the next puzzle for the authenticated user.

        The user's puzzle rating and history influence the puzzle choice.
        Optionally, a puzzle rating can be specified, overriding the user's rating.

        Requires authentication (OAuth scope: `puzzle:read`).

        https://lichess.org/api#tag/Puzzles/operation/apiPuzzleNext

        :param rating: Optional puzzle rating to target. If omitted, the user's
                       current puzzle rating is used.
        :return: A dictionary containing the puzzle details and the source game.
        """
        path = "/api/puzzle/next"
        params = {"rating": rating} if rating is not None else {}
        # Note: Authentication is handled by the underlying session/requester
        # when the berserk.Client is initialized with a token.
        # The Lichess API uses POST for this endpoint.
        response = self._r.post(path, params=params)
        return cast(NextPuzzle, response)
