from typing import List, cast
from ..types.fide import FidePlayer
from .base import BaseClient


class Fide(BaseClient):
    def search_players(self, name: str) -> List[FidePlayer]:
        """Search for FIDE players by name.

        :param name: name (or partial name) of the player
        :return: a list of matching FIDE players
        """
        path = "/api/fide/player"
        params = {"q": name}
        data = self._r.get(path, params=params)
        return cast(List[FidePlayer], data)

    def get_player(self, player_id: int) -> FidePlayer:
        """Get detailed FIDE player data by ID.

        :param player_id: FIDE player ID
        :return: FIDE player data
        """
        path = f"/api/fide/player/{player_id}"
        data = self._r.get(path)
        return cast(FidePlayer, data)
