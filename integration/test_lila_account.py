import berserk
import pytest

BASE_URL = "http://bdit_lila:9663"

@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession('lip_bobby')
    client = berserk.Client(
        session, base_url=BASE_URL)
    yield client


def test_account_get(client):
    me = client.account.get()
    assert me['id'] == 'bobby'


def test_account_get_email(client):
    assert client.account.get_email() == 'bobby@localhost'


def test_account_get_preferences(client):
    preferences = client.account.get_preferences()
    assert preferences['language'] == 'en-US'
    assert preferences['prefs']['animation'] == 2


def test_account_kid_mode(client):
    assert client.account.get_kid_mode() == False
    client.account.set_kid_mode(True)
    assert client.account.get_kid_mode() == True


def test_account_upgrade_to_bot():
    session = berserk.TokenSession('lip_zerogames')
    client = berserk.Client(
        session, base_url=BASE_URL)
    assert 'title' not in client.account.get()
    client.account.upgrade_to_bot()
    assert client.account.get()['title'] == "BOT"
