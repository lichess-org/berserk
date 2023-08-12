import pytest

from berserk import Client, Team
from utils import validate


class TestLichessGames:
    @pytest.mark.vcr
    def test_get_team(self):
        res = Client().teams.get_team("lichess-swiss")
        validate(Team, res)

    @pytest.mark.vcr
    def teams_of_player(self):
        res = Client().teams.teams_of_player("Lichess")
        validate(list[Team], res)