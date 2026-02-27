import pytest

from berserk import Client, TokenSession
from utils import validate


class TestGames:
    @pytest.mark.vcr
    def test_export_bookmarks(self):
        res = list(Client(session=TokenSession("fake-token")).games.export_bookmarks())
        assert len(res) >= 1
        assert "id" in res[0]

    @pytest.mark.vcr
    def test_export_bookmarks_pgn(self):
        res = list(
            Client(session=TokenSession("fake-token")).games.export_bookmarks(as_pgn=True)
        )
        assert len(res) >= 1
        assert isinstance(res[0], str)
        assert "[White" in res[0]
