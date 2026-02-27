import pytest

from berserk import Client, TokenSession


class TestChallenges:
    @pytest.mark.vcr
    def test_show(self):
        # OAuth endpoint; cassette is mocked.
        session = TokenSession(token="FAKE_TOKEN")
        res = Client(session=session).challenges.show("FAKE_CHALLENGE")
        assert res["id"] == "FAKE_CHALLENGE"
