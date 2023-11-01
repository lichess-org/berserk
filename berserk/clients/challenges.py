from __future__ import annotations

from typing import Any, Dict, List
from deprecated import deprecated

from ..types.challenges import Challenge, ChallengeDeclineReason
from ..types.common import Color, Variant
from .base import BaseClient


class Challenges(BaseClient):
    def get_mine(self) -> Dict[str, List[Challenge]]:
        """Get all outgoing challenges (created by me) and incoming challenges (targeted at me).

        Requires OAuth2 authorization with challenge:read scope.

        :return: all my outgoing and incoming challenges
        """
        path = "/api/challenge"
        return self._r.get(path)

    def create(
        self,
        username: str,
        rated: bool,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: Color | None = None,
        variant: Variant | None = None,
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
        variant: Variant | None = None,
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
        variant: Variant | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Challenge AI to a game.

        :param level: level of the AI (1 to 8)
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :param variant: game variant to use
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
        variant: Variant | None = None,
        position: str | None = None,
        rated: bool | None = None,
        name: str | None = None,
    ) -> Dict[str, Any]:
        """Create a challenge that any two players can join.

        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param variant: game variant to use
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

    def cancel(self, challenge_id: str, opponent_token: str | None = None) -> None:
        """Cancel an outgoing challenge, or abort the game if challenge was accepted but the game was not yet played.

        Requires OAuth2 authorization with challenge:write, bot:play and board:play scopes.

        :param challenge_id: ID of a challenge
        :param opponent_token: if set to the challenge:write token of the opponent, allows game to be cancelled
            even if both players have moved
        """
        path = f"/api/challenge/{challenge_id}/cancel"
        params = {"opponentToken": opponent_token}
        self._r.post(path=path, params=params)

    def start_clocks(
        self, game_id: str, token_player_1: str, token_player_2: str
    ) -> None:
        """Starts the clocks of a game immediately, even if a player has not yet made a move.

        Requires the OAuth tokens of both players with challenge:write scope. The tokens can be in any order.

        If the clocks have already started, the call will have no effect.

        :param game_id: game ID
        :param token_player_1: OAuth token of player 1 with challenge:write scope
        :param token_player_2: OAuth token of player 2 with challenge:write scope
        """
        path = f"/api/challenge/{game_id}/start-clocks"
        params = {"token1": token_player_1, "token2": token_player_2}
        self._r.post(path=path, params=params)

    def add_time_to_opponent_clock(self, game_id: str, seconds: int) -> None:
        """Add seconds to the opponent's clock. Can be used to create games with time odds.

        Requires OAuth2 authorization with challenge:write scope.

        :param game_id: game ID
        :param seconds: number of seconds to add to opponent's clock
        """
        path = f"/api/round/{game_id}/add-time/{seconds}"
        self._r.post(path)

    def create_tokens_for_multiple_users(
        self, usernames: List[str], description: str
    ) -> Dict[str, str]:
        """This endpoint can only be used by Lichess admins.

        Create and obtain challenge:write tokens for multiple users.

        If a similar token already exists for a user, it is reused. This endpoint is idempotent.

        :param usernames: List of usernames
        :param description: user-visible token description
        :return: challenge:write tokens of each user
        """
        path = "/api/token/admin-challenge"
        payload = {"users": ",".join(usernames), "description": description}
        return self._r.post(path=path, payload=payload)
