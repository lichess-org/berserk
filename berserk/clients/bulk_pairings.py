from __future__ import annotations

from typing import cast

from ..enums import Variant
from ..formats import JSON, JSON_LIST
from ..types.bulk_pairings import BulkPairing
from .base import BaseClient


class BulkPairings(BaseClient):
    """Client for bulk pairing related endpoints."""

    def get_upcoming(self) -> list[BulkPairing]:
        """Get a list of upcoming bulk pairings you created.

        Only bulk pairings that are scheduled in the future, or that have a clock start scheduled in the future, are listed.

        Bulk pairings are deleted from the server after the pairings are done and the clocks have started.

        :return: list of your upcoming bulk pairings.
        """
        path = "/api/bulk-pairing"
        return cast(list[BulkPairing], self._r.get(path, fmt=JSON_LIST))

    def create(
        self,
        token_pairings: list[tuple[str, str]],
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        pair_at: int | None = None,
        start_clocks_at: int | None = None,
        rated: bool = False,
        variant: Variant | None = None,
        fen: str | None = None,
        message: str | None = None,
        rules: list[str] | None = None,
    ) -> BulkPairing:
        """Create a bulk pairing.

        :param players_tokens: players OAuth tokens
        :param clock_limit: clock initial time
        :param clock_increment: clock increment
        :param days: days per turn (for correspondence)
        :param pair_at: date at which the games will be created as a milliseconds unix timestamp. Up to 7 days in the future. Defaults to now.
        :param start_clocks_at: date at which the clocks will be automatically started as a Unix timestamp in milliseconds.
            Up to 7 days in the future. Note that the clocks can start earlier than specified, if players start making moves in the game.
            If omitted, the clocks will not start automatically.
        :param rated: set to true to make the games rated. defaults to false.
        :param variant: variant of the games
        :param fen: custom initial position (in FEN). Only allowed if variant is standard, fromPosition, or chess960 (if a valid 960 starting position), and the games cannot be rated.
        :param message: message sent to players when their game is created
        :param rules: extra game rules
        :return: the newly created bulk pairing
        """
        path = "/api/bulk-pairing"
        payload = {
            "players": ",".join(":".join(pair) for pair in token_pairings),
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "pairAt": pair_at,
            "startClocksAt": start_clocks_at,
            "rated": rated,
            "variant": variant,
            "fen": fen,
            "message": message,
            "rules": ",".join(rules) if rules else None,
        }
        return cast(
            BulkPairing,
            self._r.post(
                path,
                payload=payload,
                fmt=JSON,
            ),
        )

    def start_clocks(self, bulk_pairing_id: str) -> None:
        """Immediately start all clocks of the games of the given bulk pairing.

        This overrides the startClocksAt value of an existing bulk pairing.

        If the games have not yet been created (pairAt is in the future) or the clocks
        have already started (startClocksAt is in the past), then this does nothing.

        :param bulk_pairing_id: id of the bulk pairing to start clocks of
        """
        path = f"/api/bulk-pairing/{bulk_pairing_id}/start-clocks"
        self._r.post(path)

    def cancel(self, bulk_pairing_id: str) -> None:
        """Cancel and delete a bulk pairing that is scheduled in the future.

        If the games have already been created, then this does nothing.

        :param bulk_pairing_id: id of the bulk pairing to cancel
        """
        path = f"/api/bulk-pairing/{bulk_pairing_id}"
        self._r.request("DELETE", path)
