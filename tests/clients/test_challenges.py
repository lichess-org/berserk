from urllib.parse import parse_qs

import requests_mock

from berserk import Client


class TestChallenges:
    def test_create_tokens_for_multiple_users_sends_form_body(self):
        with requests_mock.Mocker() as m:
            m.post(
                "https://lichess.org/api/token/admin-challenge",
                json={"alice": "lip_a", "bob": "lip_b"},
            )
            Client().challenges.create_tokens_for_multiple_users(
                ["alice", "bob"], "Test tournament"
            )
            assert (
                m.last_request.headers["Content-Type"]
                == "application/x-www-form-urlencoded"
            )
            assert parse_qs(m.last_request.text) == {
                "users": ["alice,bob"],
                "description": ["Test tournament"],
            }
