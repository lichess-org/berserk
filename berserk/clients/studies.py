from __future__ import annotations

from typing import Iterator

from ..formats import PGN
from .base import BaseClient


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(self, study_id: str, chapter_id: str) -> str:
        """Export one chapter of a study.

        :return: chapter PGN
        """
        path = f"/api/study/{study_id}/{chapter_id}.pgn"
        return self._r.get(path, fmt=PGN)

    def export(self, study_id: str) -> Iterator[str]:
        """Export all chapters of a study.

        :return: iterator over all chapters as PGN
        """
        path = f"/api/study/{study_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)

    def by_username(self, username: str) -> Iterator[str]:
        """Export all chapters of a study.

        return:iterator over all chapters as PGN"""
        path = f"/study/by/{username}/export.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)
