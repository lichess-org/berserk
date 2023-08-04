import pytest

from berserk import Client, TeamType
from pydantic import TypeAdapter


class TestLichessGames:
    @pytest.mark.vcr
    def test_get_team(self):
        res = Client().teams.get_team("lichess-swiss")
        # print(json.dumps(res))
        # res2 = json.loads(json.dumps(res))
        validate(TeamType, res)

    @pytest.mark.vcr
    def teams_of_player(self):
        res = Client().teams.teams_of_player("Lichess")
        validate(list[TeamType], res)


# Should be in a util file once used by more tests
def validate(t, value):
    return TypeAdapter(t).validate_python(value)
