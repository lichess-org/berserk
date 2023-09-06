from __future__ import annotations

from time import time as now
from typing import Iterator, Any, Dict, Tuple, List, Literal

from .. import models
from ..types.common import Color, Variant
from ..formats import TEXT, JSON_LIST
from .base import BaseClient


class Board(BaseClient):
    """Client for physical board or external application endpoints."""

    def stream_incoming_events(self) -> Iterator[Dict[str, Any]]:
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        """
        path = "/api/stream/event"
        yield from self._r.get(path, stream=True)

    def seek(
        self,
        time: int,
        increment: int,
        rated: bool = False,
        variant: Variant = "standard",
        color: Color | Literal["random"] = "random",
        rating_range: str | Tuple[int, int] | List[int] | None = None,
    ) -> float:
        """Create a public seek to start a game with a random opponent.

        :param time: initial clock time in minutes
        :param increment: clock increment in minutes
        :param rated: whether the game is rated (impacts ratings)
        :param variant: game variant to use
        :param color: color to play
        :param rating_range: range of opponent ratings
        :return: duration of the seek
        """
        if isinstance(rating_range, (list, tuple)):
            low, high = rating_range
            rating_range = f"{low}-{high}"

        path = "/api/board/seek"
        payload = {
            "rated": str(bool(rated)).lower(),
            "time": time,
            "increment": increment,
            "variant": variant,
            "color": color,
            "ratingRange": rating_range or "",
        }

        # we time the seek
        start = now()

        # just keep reading to keep the search going
        for _ in self._r.post(path, data=payload, fmt=TEXT, stream=True):
            pass

        # and return the time elapsed
        return now() - start

    def stream_game_state(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Get the stream of events for a board game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"/api/board/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def make_move(self, game_id: str, move: str) -> None:
        """Make a move in a board game.

        :param game_id: ID of a game
        :param move: move to make
        """
        path = f"/api/board/game/{game_id}/move/{move}"
        self._r.post(path)

    def post_message(self, game_id: str, text: str, spectator: bool = False) -> None:
        """Post a message in a board game.

        :param game_id: ID of a game
        :param text: text of the message
        :param spectator: post to spectator room (else player room)
        """
        path = f"/api/board/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        self._r.post(path, json=payload)

    def get_game_chat(self, game_id: str) -> List[Dict[str, str]]:
        """Get the messages posted in the game chat.

        :param str game_id: ID of a game
        :return: list of game chat events
        """
        path = f"/api/board/game/{game_id}/chat"
        return self._r.get(path, fmt=JSON_LIST)

    def abort_game(self, game_id: str) -> None:
        """Abort a board game.

        :param game_id: ID of a game
        """
        path = f"/api/board/game/{game_id}/abort"
        self._r.post(path)

    def resign_game(self, game_id: str) -> None:
        """Resign a board game.

        :param game_id: ID of a game
        """
        path = f"/api/board/game/{game_id}/resign"
        self._r.post(path)

    def handle_draw_offer(self, game_id: str, accept: bool) -> None:
        """Create, accept, or decline a draw offer.

        To offer a draw, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a draw offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        draw offer.

        Often, it's easier to call :func:`offer_draw`, :func:`accept_draw`, or
        :func:`decline_draw`.

        :param game_id: ID of an in-progress game
        :param accept: whether to accept
        """
        accept_str = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/draw/{accept_str}"
        self._r.post(path)

    def offer_draw(self, game_id: str) -> None:
        """Offer a draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, True)

    def accept_draw(self, game_id: str) -> None:
        """Accept an already offered draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, True)

    def decline_draw(self, game_id: str) -> None:
        """Decline an already offered draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, False)

    def handle_takeback_offer(self, game_id: str, accept: bool) -> None:
        """Create, accept, or decline a takeback offer.

        To offer a takeback, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a takeback offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        takeback offer.

        Often, it's easier to call :func:`offer_takeback`, :func:`accept_takeback`, or
        :func:`decline_takeback`.

        :param game_id: ID of an in-progress game
        :param accept: whether to accept
        """
        accept_str = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/takeback/{accept_str}"
        self._r.post(path)

    def offer_takeback(self, game_id: str) -> None:
        """Offer a takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, True)

    def accept_takeback(self, game_id: str) -> None:
        """Accept an already offered takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, True)

    def decline_takeback(self, game_id: str) -> None:
        """Decline an already offered takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, False)

    def claim_victory(self, game_id: str) -> None:
        """Claim victory when the opponent has left the game for a while.

        Generally, this should only be called once the `opponentGone` event
        is received in the board game state stream and the `claimWinInSeconds`
        time has elapsed.

        :param str game_id: ID of an in-progress game
        """
        path = f"/api/board/game/{game_id}/claim-victory/"
        self._r.post(path)

    def go_berserk(self, game_id: str) -> None:
        """Go berserk on an arena tournament game.

        :param str game_id: ID of an in-progress game
        """
        path = f"/api/board/game/{game_id}/berserk"
        self._r.post(path)
