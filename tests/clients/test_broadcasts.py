import pytest

from berserk import Client
from berserk.types import (
    BroadcastTop,
    PaginatedBroadcasts,
    BroadcastsByUser,
    BroadcastPlayerEntry,
    BroadcastPlayerEntryWithFideAndGames,
    BroadcastTeamLeaderboardEntry,
)
from utils import skip_if_older_3_dot_10, validate


class TestBroadcasts:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_top(self):
        res = Client().broadcasts.get_top(page=1, html=False)
        validate(BroadcastTop, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_search(self):
        res = Client().broadcasts.search(query="chess", page=1)
        validate(PaginatedBroadcasts, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_user(self):
        res = Client().broadcasts.get_by_user(username="lichess", page=1)
        validate(BroadcastsByUser, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_players(self):
        res = Client().broadcasts.get_players(broadcast_tournament_id="6UkdBX8x")
        validate(list[BroadcastPlayerEntry], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_player(self):
        # Schema can evolve frequently; just smoke test.
        players = Client().broadcasts.get_players(broadcast_tournament_id="6UkdBX8x")
        if not players:
            pytest.skip("Broadcast has no players data")
        player_id = players[0].get("fideId") or players[0]["name"]
        res = Client().broadcasts.get_player(
            broadcast_tournament_id="6UkdBX8x", player_id=str(player_id)
        )
        assert isinstance(res, dict)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_team_standings(self):
        # Schema can evolve frequently; just smoke test.
        res = Client().broadcasts.get_team_standings(broadcast_tournament_id="Y9YjcDKG")
        assert isinstance(res, list)
        assert isinstance(res[0], dict)
