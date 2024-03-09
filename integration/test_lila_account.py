import berserk
import pytest

@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession('lip_bobby')
    client = berserk.Client(session, base_url="http://lila:9663")
    yield client


def test_account_get(client):
    me = client.account.get()
    assert me['id'] == 'bobby'


def test_account_get_email(client):
    assert client.account.get_email() == 'bobby@localhost'


def test_update_kid_mode(client):
    assert client.account.get_kid_mode() == False
    client.account.set_kid_mode(True)
    assert client.account.get_kid_mode() == True
