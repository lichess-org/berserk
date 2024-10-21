from __future__ import annotations

from typing import cast, List, Iterator

from ..formats import PGN
from ..types.common import Color, Variant
from ..types import ChapterIdName
from .base import BaseClient


def append_query_params(
    url: str,
    clocks: bool,
    comments: bool,
    variations: bool,
    source: bool,
    orientation: bool,
) -> str:
    pairs = {
        "clocks": clocks,
        "comments": comments,
        "variations": variations,
        "source": source,
        "orientation": orientation,
    }
    return f"{url}?" + "&".join(f"{k}={str(pairs[k]).lower()}" for k in pairs)


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(
        self,
        study_id: str,
        chapter_id: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> str:
        """Export one chapter of a study.

        :return: chapter PGN
        """
        path = append_query_params(
            f"/api/study/{study_id}/{chapter_id}.pgn",
            clocks,
            comments,
            variations,
            source,
            orientation,
        )
        return self._r.get(path, fmt=PGN)

    def export(
        self,
        study_id: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> Iterator[str]:
        """Export all chapters of a study.

        :return: iterator over all chapters as PGN
        """
        path = append_query_params(
            f"/api/study/{study_id}.pgn",
            clocks,
            comments,
            variations,
            source,
            orientation,
        )
        yield from self._r.get(path, fmt=PGN, stream=True)

    def export_by_username(
        self,
        username: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> Iterator[str]:
        """Export all chapters of all studies of a user in PGN format.

        If authenticated, then all public, unlisted, and private studies are included.

        If not, only public (non-unlisted) studies are included.

        return:iterator over all chapters as PGN"""
        path = append_query_params(
            f"/study/by/{username}/export.pgn",
            clocks,
            comments,
            variations,
            source,
            orientation,
        )
        yield from self._r.get(path, fmt=PGN, stream=True)

    def import_pgn(
        self,
        study_id: str,
        chapter_name: str,
        pgn: str,
        orientation: Color = "white",
        variant: Variant = "standard",
    ) -> List[ChapterIdName]:
        """Imports arbitrary PGN into an existing study.
        Creates a new chapter in the study.

        If the PGN contains multiple games (separated by 2 or more newlines) then multiple chapters will be created within the study.

        Note that a study can contain at most 64 chapters.

        return: List of the chapters {id, name}"""
        # https://lichess.org/api/study/{studyId}/import-pgn
        path = f"/api/study/{study_id}/import-pgn"
        payload = {
            "name": chapter_name,
            "pgn": pgn,
            "orientation": orientation,
            "variant": variant,
        }
        # The return is of the form:
        return cast(
            List[ChapterIdName], self._r.post(path, data=payload).get("chapters", [])
        )
