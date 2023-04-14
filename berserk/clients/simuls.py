# -*- coding: utf-8 -*-
"""Simuls-related endpoints."""
from __future__ import annotations

from .base import BaseClient


class Simuls(BaseClient):
    """Simultaneous exhibitions - one vs many."""

    def get(self):
        """Get recently finished, ongoing, and upcoming simuls.

        :return: current simuls
        :rtype: list[dict[str, Any]]
        """
        path = "api/simul"
        return self._r.get(path)
