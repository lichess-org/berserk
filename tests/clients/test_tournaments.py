import pytest

from berserk import ArenaResult, Client, SwissResult
from typing import List

from berserk.types.tournaments import TeamBattleResult
from utils import validate, skip_if_older_3_dot_10


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_swiss_result(self):
        res = list(Client().tournaments.stream_swiss_results("ADAHHiMX", limit=3))
        validate(List[SwissResult], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_arenas_result(self):
        res = list(Client().tournaments.stream_results("hallow23", limit=3))
        validate(List[ArenaResult], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_team_standings(self):
        res = list(Client().tournaments.get_team_standings("fake"))
        validate(TeamBattleResult, res)
