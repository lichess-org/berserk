import berserk
import pytest

@pytest.fixture(scope="module")
def client():
    client = berserk.Client(base_url="http://lila:9663")
    yield client


def test_account_get(client):
    top_10 = client.users.get_all_top_10()
    assert len(top_10['bullet']) == 10
