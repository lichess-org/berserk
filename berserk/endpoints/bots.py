# -*- coding: utf-8 -*-
"""Bot-related endpoints."""
from .. import models
from ..enums import Reason
from . import BaseClient


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self):
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        :rtype: iterator over the stream of events
        """
        path = "api/stream/event"
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id):
        """Get the stream of events for a bot game.

        :param str game_id: ID of a game
        :return: iterator over game states
        """
        path = f"api/bot/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def make_move(self, game_id, move):
        """Make a move in a bot game.

        :param str game_id: ID of a game
        :param str move: move to make
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/move/{move}"
        return self._r.post(path)["ok"]

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a bot game.

        :param str game_id: ID of a game
        :param str text: text of the message
        :param bool spectator: post to spectator room (else player room)
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        return self._r.post(path, json=payload)["ok"]

    def abort_game(self, game_id):
        """Abort a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/abort"
        return self._r.post(path)["ok"]

    def resign_game(self, game_id):
        """Resign a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/resign"
        return self._r.post(path)["ok"]

    def accept_challenge(self, challenge_id):
        """Accept an incoming challenge.

        :param str challenge_id: ID of a challenge
        :return: success
        :rtype: bool
        """
        path = f"api/challenge/{challenge_id}/accept"
        return self._r.post(path)["ok"]

    def decline_challenge(self, challenge_id, reason=Reason.GENERIC):
        """Decline an incoming challenge.
        :param str challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        :type reason: :class:`~berserk.enums.Reason`
        :return: success indicator
        :rtype: bool
        """
        path = f"api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        return self._r.post(path, json=payload)["ok"]
