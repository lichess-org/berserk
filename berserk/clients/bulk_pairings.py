"""Bulk pairings client"""
from __future__ import annotations

from typing import Any, cast, Dict, List, Optional

from .base import BaseClient
from ..enums import Variant
from ..formats import JSON_LIST, JSON
from ..types.bulk_pairings import BulkPairingGame
from ..types.core.aliases import LichessID
from ..types.core.common import Result


class BulkPairings(BaseClient):
    """Client for bluk pairing related endpoints."""

    def view_upcoming(self) -> List[BulkPairingGame]:
        """View upcoming bulk pairings.

        :return: List of upcoming bulk pairings.
        :rtype: List[BulkPairingGame]
        """
        path: str = "/api/bulk-pairing"
        return cast(List[BulkPairingGame], self._r.get(path, fmt=JSON_LIST))

    def create(
        self,
        players_tokens: List[str],
        clock_limit: int,
        clock_increment: int,
        days: Optional[int] = None,
        pair_at: Optional[int] = None,
        start_clocks_at: Optional[int] = None,
        rated: Optional[bool] = None,
        variant: Optional[Variant] = None,
        fen: Optional[str] = None,
        message: Optional[str] = None,
        rules: Optional[list[str]] = None,
    ) -> BulkPairingGame:
        """Create a bulk pairing.

        :param List[str] players_tokens: players OAuth tokens
        :param int clock_limit: clock initial time
        :param int clock_increment: clock increment
        :param Optional[int] days: days per turn (correspondence)
        :param Optional[int] pair_at: day at wich game will be created
        :param Optional[int] start_clocks_at: day at wich clocks will start
        :param Optional[bool] rated: rated or casual
        :param Optional[Variant] variant: game variant
        :param Optional[str] fen: starting fen
        :param Optional[str] message: message sent to players
        :param Optional[list[str]] rules: extra game rules
        :return BulkPairingGame: the pairing created
        """
        path: str = "/api/bulk-pairing"
        payload: Dict[str, Any] = {
            "players": ":".join(players_tokens),
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
            BulkPairingGame,
            self._r.post(
                path,
                payload=payload,
                fmt=JSON,
            ),
        )

    def start_clocks(self, pairing_id: LichessID) -> Result:
        """Manually start clocks.

        :param LichessID pairing_id: pairing to start clocks of
        :return Result: operation result
        """
        path: str = f"https://lichess.org/api/bulk-pairing/{pairing_id}/start-clocks"
        return cast(Result, self._r.post(path, fmt=JSON))

    def cancel(self, pairing_id: LichessID) -> Result:
        """Cancel a bulk pairing.

        :param LichessID pairing_id: pairing to cancel
        :return Result: operation result
        """
        path: str = f"https://lichess.org/api/bulk-pairing/{pairing_id}"
        return cast(Result, self._r.request("DELETE", path, fmt=JSON))
