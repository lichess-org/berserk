import berserk
import pytest

BASE_URL = "http://bdit_lila:8080"


@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession("lip_bobby")
    client = berserk.Client(session, base_url=BASE_URL)
    yield client


def test_export_imported_games(client):
    res = client.games.export_imported()
    assert isinstance(res, str)
