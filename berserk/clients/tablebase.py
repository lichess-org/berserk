from __future__ import annotations

from typing import Any, Dict, Literal
import requests

from .base import BaseClient

TABLEBASE_URL = "https://tablebase.lichess.ovh"


class Tablebase(BaseClient):
    """Client for tablebase related endpoints."""

    def __init__(self, session: requests.Session, tablebase_url: str | None = None):
        super().__init__(session, tablebase_url or TABLEBASE_URL)

    def look_up(
        self,
        position: str,
        variant: Literal["standard"]
        | Literal["atomic"]
        | Literal["antichess"] = "standard",
    ) -> Dict[str, Any]:
        """Look up the tablebase result for a position.

        :param position: FEN of the position to look up
        :param variant: the variant of the position to look up (supported are standard,
            atomic, and antichess)
        :return: tablebase information about this position
        """
        path = f"/{variant}"
        params = {"fen": position}
        return self._r.get(path, params=params)

    def standard(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for a standard chess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "standard")

    def atomic(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for an atomic chess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "atomic")

    def antichess(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for an antichess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "antichess")
