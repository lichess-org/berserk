import pytest

from berserk import Client, TokenSession


class TestGames:
    @pytest.mark.vcr
    def test_export_bookmarks_pgn(self):
        # OAuth endpoint; cassette is mocked.
        session = TokenSession(token="FAKE_TOKEN")
        res = list(Client(session=session).games.export_bookmarks(as_pgn=True, max=1))
        assert isinstance(res[0], str)

    @pytest.mark.vcr
    def test_export_bookmarks_ndjson(self):
        session = TokenSession(token="FAKE_TOKEN")
        res = list(Client(session=session).games.export_bookmarks(as_pgn=False, max=1))
        assert isinstance(res[0], dict)
