from __future__ import annotations

from typing import Any, Dict

from .base import BaseClient


class Simuls(BaseClient):
    """Simultaneous exhibitions - one vs many."""

    def get(self) -> Dict[str, Any]:
        """Get recently finished, ongoing, and upcoming simuls.

        :return: current simuls
        """
        path = "/api/simul"
        return self._r.get(path)
