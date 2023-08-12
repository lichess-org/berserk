import pytest

from berserk import Client, Team
from pydantic import TypeAdapter


class TestLichessGames:
    @pytest.mark.vcr
    def test_get_team(self):
        res = Client().teams.get_team("lichess-swiss")
        validate(Team, res)

    @pytest.mark.vcr
    def teams_of_player(self):
        res = Client().teams.teams_of_player("Lichess")
        validate(list[Team], res)


# Should be in a util file once used by more tests
def validate(t, value):
    # TODO: check exactly what `strict=True` enforce
    return TypeAdapter(t).validate_python(value,strict=True)
