# -*- coding: utf-8 -*-
"""Studies-related endpoints."""
from __future__ import annotations

from typing import Iterator

from ..formats import PGN
from .base import BaseClient


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(self, study_id: str, chapter_id: str) -> str:
        """Export one chapter of a study.

        :param str study_id: the study ID
        :param str chapter_id: the chapter ID
        :return str: chapter as PGN
        """
        path = f"/study/{study_id}/{chapter_id}.pgn"
        return self._r.get(path, fmt=PGN)

    def export(self, study_id: str) -> Iterator[str]:
        """Export all chapters of a study.

        :param str study_id: the study ID
        :return Iterator[str]: all chapters as PGN
        """
        path = f"/study/{study_id}.pgn"
        return self._r.get(path, fmt=PGN, stream=True)
