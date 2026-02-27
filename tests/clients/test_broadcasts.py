import pytest

from berserk import Client, TokenSession
from berserk.types import (
    BroadcastTop,
    PaginatedBroadcasts,
    BroadcastsByUser,
    BroadcastPlayerEntry,
    BroadcastPlayerEntryWithFideAndGames,
    BroadcastTeamLeaderboardEntry,
)
from typing import List
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

    @pytest.mark.vcr
    def test_reset_round(self):
        # reset_round returns None on success (consumes {"ok": true})
        Client(session=TokenSession("fake-token")).broadcasts.reset_round("testRound1")

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_players(self):
        res = Client().broadcasts.get_players("ZfhmG9VB")
        validate(List[BroadcastPlayerEntry], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_player(self):
        res = Client().broadcasts.get_player("ZfhmG9VB", "1503014")
        validate(BroadcastPlayerEntryWithFideAndGames, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_team_standings(self):
        res = Client().broadcasts.get_team_standings("ZfhmG9VB")
        validate(List[BroadcastTeamLeaderboardEntry], res)
