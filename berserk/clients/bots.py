from __future__ import annotations

from typing import Iterator, Any, Dict

from .. import models
from ..formats import NDJSON
from .base import BaseClient
from ..types.common import ChallengeDeclineReason


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self) -> Iterator[Dict[str, Any]]:
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        """
        path = "/api/stream/event"
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Get the stream of events for a bot game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"/api/bot/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def get_online_bots(self, limit: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream the online bot users.

        :param limit: Maximum number of bot users to fetch
        :return: iterator over online bots
        """
        path = "/api/bot/online"
        params = {"nb": limit}
        yield from self._r.get(
            path, params=params, stream=True, fmt=NDJSON, converter=models.User.convert
        )

    def make_move(self, game_id: str, move: str) -> None:
        """Make a move in a bot game.

        :param game_id: ID of a game
        :param move: move to make
        """
        path = f"/api/bot/game/{game_id}/move/{move}"
        self._r.post(path)

    def post_message(self, game_id: str, text: str, spectator: bool = False):
        """Post a message in a bot game.

        :param game_id: ID of a game
        :param text: text of the message
        :param spectator: post to spectator room (else player room)
        """
        path = f"/api/bot/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        self._r.post(path, json=payload)

    def abort_game(self, game_id: str) -> None:
        """Abort a bot game.

        :param game_id: ID of a game
        """
        path = f"/api/bot/game/{game_id}/abort"
        self._r.post(path)

    def resign_game(self, game_id: str) -> None:
        """Resign a bot game.

        :param game_id: ID of a game
        """
        path = f"/api/bot/game/{game_id}/resign"
        self._r.post(path)

    def accept_challenge(self, challenge_id: str) -> None:
        """Accept an incoming challenge.

        :param challenge_id: ID of a challenge
        """
        path = f"/api/challenge/{challenge_id}/accept"
        self._r.post(path)

    def decline_challenge(
        self, challenge_id: str, reason: ChallengeDeclineReason = "generic"
    ) -> None:
        """Decline an incoming challenge.

        :param challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        """
        path = f"/api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        self._r.post(path, json=payload)
