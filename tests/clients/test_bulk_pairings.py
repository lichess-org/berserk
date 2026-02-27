import pytest

from berserk import Client, TokenSession


class TestBulkPairings:
    @pytest.mark.vcr
    def test_get_games_pgn(self):
        # OAuth endpoint; cassette is mocked.
        session = TokenSession(token="FAKE_TOKEN")
        res = list(Client(session=session).bulk_pairings.get_games("FAKE_BULK", as_pgn=True))
        assert isinstance(res[0], str)

    @pytest.mark.vcr
    def test_get_games_ndjson(self):
        session = TokenSession(token="FAKE_TOKEN")
        res = list(Client(session=session).bulk_pairings.get_games("FAKE_BULK", as_pgn=False))
        assert isinstance(res[0], dict)
