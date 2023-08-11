from __future__ import annotations

from typing import Any, Dict, Generator, Iterator

from ..formats import PGN, JSON
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

    def get_study_by_username(
        self, username: str
    ) -> Generator[Dict[str, Any], None, None]:
        # end point for api/study/by/{username}
        path = f"/api/study/by/{username}"
        yield from self._r.get(path, fmt=JSON, stream=True)