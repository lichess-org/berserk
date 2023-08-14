import pytest

from berserk import Client, Team, PaginatedTeams
from typing import List
from utils import validate, skip_if_older_3_dot_10


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_team(self):
        res = Client().teams.get_team("lichess-swiss")
        validate(Team, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_teams_of_player(self):
        res = Client().teams.teams_of_player("Lichess")
        validate(List[Team], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_popular(self):
        res = Client().teams.get_popular()
        validate(PaginatedTeams, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_search(self):
        res = Client().teams.search("lichess")
        validate(PaginatedTeams, res)
