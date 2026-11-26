from urllib.parse import parse_qs

import pytest
import requests_mock

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


class TestTeamMessaging:
    def test_message_all_members_sends_form_body(self):
        with requests_mock.Mocker() as m:
            m.post("https://lichess.org/team/some-team/pm-all", json={"ok": True})
            Client().teams.message_all_members("some-team", "hello team")
            assert (
                m.last_request.headers["Content-Type"]
                == "application/x-www-form-urlencoded"
            )
            assert parse_qs(m.last_request.text) == {"message": ["hello team"]}
