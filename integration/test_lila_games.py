import berserk
import pytest
from tests.clients.utils import validate

BASE_URL = "http://bdit_lila:8080"


@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession("lip_bobby")
    client = berserk.Client(session, base_url=BASE_URL)
    yield client


class TestGames:
    def test_export_imported_games(self, client):
        res = client.games.export_imported()
        validate(str, res)
