from __future__ import annotations

from typing import cast
import requests
import logging

from .base import BaseClient
from ..types import (
    OpeningStatistic,
    OpeningExplorerVariant,
    Speed,
    OpeningExplorerRating,
)

logger = logging.getLogger("berserk.client.opening_explorer")

EXPLORER_URL = "https://explorer.lichess.ovh"


class OpeningExplorer(BaseClient):
    """Openings explorer endpoints."""

    def __init__(self, session: requests.Session, explorer_url: str | None = None):
        super().__init__(session, explorer_url or EXPLORER_URL)

    def get_lichess_games(
        self,
        variant: OpeningExplorerVariant = "standard",
        position: str | None = None,
        play: str | None = None,
        speeds: list[Speed] | None = None,
        ratings: list[OpeningExplorerRating] | None = None,
        since: str | None = None,
        until: str | None = None,
        moves: int | None = None,
        top_games: int | None = None,
        recent_games: int | None = None,
        history: bool | None = None,
    ) -> OpeningStatistic:
        """Get most played move from a position based on lichess games."""

        path = "/lichess"

        if top_games and top_games >= 4:
            logger.warn(
                "The Lichess API caps the top games parameter to 4 (you requested %d)",
                top_games,
            )

        if recent_games and recent_games >= 4:
            logger.warn(
                "The Lichess API caps the recent games parameter to 4 (you requested %d)",
                recent_games,
            )

        params = {
            "variant": variant,
            "fen": position,
            "play": play,
            "speeds": ",".join(speeds) if speeds else None,
            "ratings": ",".join(ratings) if ratings else None,
            "since": since,
            "until": until,
            "moves": moves,
            "topGames": top_games,
            "recentGames": recent_games,
            "history": history,
        }
        return cast(OpeningStatistic, self._r.get(path, params=params))
