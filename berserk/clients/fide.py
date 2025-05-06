from typing import List
from .. import models
from ..formats import JSON, JSON_LIST
from .base import BaseClient

class Fide(BaseClient):
    def search_players(self, query: str) -> List[models.FidePlayer]:
        """Search for FIDE players by query.

        :param query: full or partial name of the player
        :return: a list of matching FIDE players
        """
        path = "/api/fide/player"
        params = {"q": query}
        return self._r.get(
            path, params=params, fmt=JSON_LIST, converter=models.FidePlayer.convert
        )

    def get_player(self, player_id: int) -> models.FidePlayer:
        """Get detailed FIDE player data by ID.

        :param player_id: FIDE player ID
        :return: FIDE player data
        """
        path = f"/api/fide/player/{player_id}"
        return self._r.get(
            path, fmt=JSON, converter=models.FidePlayer.convert
        )
