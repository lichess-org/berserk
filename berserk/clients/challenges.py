from __future__ import annotations

from typing import Any, Dict
from deprecated import deprecated

from ..types.common import ChallengeDeclineReason, Color
from .base import BaseClient


class Challenges(BaseClient):
    def create(
        self,
        username: str,
        rated: bool,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: Color | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Challenge another player to a game.

        :param username: username of the player to challenge
        :param rated: whether or not the game will be rated
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :return: challenge data
        """
        path = f"/api/challenge/{username}"
        payload = {
            "rated": rated,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload)

    @deprecated(version="0.12.7")
    def create_with_accept(
        self,
        username: str,
        rated: bool,
        token: str,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: Color | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Start a game with another player.

        This is just like the regular challenge create except it forces the
        opponent to accept. You must provide the OAuth token of the opponent
        and it must have the challenge:write scope.

        :param username: username of the opponent
        :param rated: whether or not the game will be rated
        :param token: opponent's OAuth token
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :return: game data
        """
        path = f"/api/challenge/{username}"
        payload = {
            "rated": rated,
            "acceptByToken": token,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload)

    def create_ai(
        self,
        level: int = 8,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: Color | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Challenge AI to a game.

        :param level: level of the AI (1 to 8)
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: use one of the custom initial positions (variant must be
            standard and cannot be rated)
        :return: information about the created game
        """
        path = "/api/challenge/ai"
        payload = {
            "level": level,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload)

    def create_open(
        self,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        variant: str | None = None,
        position: str | None = None,
        rated: bool | None = None,
        name: str | None = None,
    ) -> Dict[str, Any]:
        """Create a challenge that any two players can join.

        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :param rated: Game is rated and impacts players ratings
        :param name: Optional name for the challenge, that players will see on
                     the challenge page.
        :return: challenge data
        """
        path = "/api/challenge/open"
        payload = {
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "variant": variant,
            "fen": position,
            "rated": rated,
            "name": name,
        }
        return self._r.post(path, json=payload)

    def accept(self, challenge_id: str) -> None:
        """Accept an incoming challenge.

        :param challenge_id: id of the challenge to accept
        """
        path = f"/api/challenge/{challenge_id}/accept"
        self._r.post(path)

    def decline(
        self, challenge_id: str, reason: ChallengeDeclineReason = "generic"
    ) -> None:
        """Decline an incoming challenge.

        :param challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        """
        path = f"/api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        self._r.post(path, json=payload)
