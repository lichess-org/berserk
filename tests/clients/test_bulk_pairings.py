import pytest

from berserk import Client, TokenSession
from utils import validate


class TestBulkPairings:
    @pytest.mark.vcr
    def test_get_games(self):
        res = list(Client(session=TokenSession("fake-token")).bulk_pairings.get_games("testBulk1"))
        assert len(res) >= 1
        assert "id" in res[0]

    @pytest.mark.vcr
    def test_get_games_pgn(self):
        res = list(
            Client(session=TokenSession("fake-token")).bulk_pairings.get_games(
                "testBulk1", as_pgn=True
            )
        )
        assert len(res) >= 1
        assert isinstance(res[0], str)
        assert "[White" in res[0]
