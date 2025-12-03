import berserk
import pytest

from utils import validate

BASE_URL = "http://bdit_lila:8080"


@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession("lip_bobby")
    client = berserk.Client(session, base_url=BASE_URL)
    yield client


def test_account_get(client):
    me = client.account.get()
    assert me["id"] == "bobby"
    validate(berserk.types.account.AccountInformation, me)


def test_account_get_email(client):
    assert client.account.get_email() == "bobby@localhost"


def test_account_get_preferences(client):
    preferences = client.account.get_preferences()
    assert preferences["language"] == "en-US"
    assert preferences["prefs"]["animation"] == 2


def test_account_kid_mode(client):
    assert not client.account.get_kid_mode()
    client.account.set_kid_mode(True)
    assert client.account.get_kid_mode()


def test_account_upgrade_to_bot():
    session = berserk.TokenSession("lip_zerogames")
    client = berserk.Client(session, base_url=BASE_URL)
    assert "title" not in client.account.get()
    client.account.upgrade_to_bot()
    assert client.account.get()["title"] == "BOT"


def test_account_follow(client):
    """Test following a user."""
    client.relations.follow("lichess")


def test_account_unfollow(client):
    """Test unfollowing a user."""
    client.relations.unfollow("lichess")


def test_account_block(client):
    """Test blocking a user."""
    client.relations.block("lichess")


def test_account_unblock(client):
    """Test unblocking a user."""
    client.relations.unblock("lichess")


def test_account_get_users_followed(client):
    """Test streaming users followed."""
    users_gen = client.relations.get_users_followed()

    first_user = next(users_gen, None)

    if first_user:
        assert "id" in first_user
        assert "username" in first_user


def test_account_get_timeline(client):
    timeline = client.account.get_timeline()
    validate(berserk.types.account.Timeline, timeline)
