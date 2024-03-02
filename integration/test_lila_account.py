import berserk

def test_account_get():
    session = berserk.TokenSession('lip_bobby')
    client = berserk.Client(session, base_url="http://lila:9663")

    me = client.account.get()
    assert me['id'] == 'bobby'


def test_account_get_email():
    session = berserk.TokenSession('lip_bobby')
    client = berserk.Client(session, base_url="http://lila:9663")

    assert client.account.get_email() == 'bobby@localhost'


def test_account_get_set_kid_mode():
    session = berserk.TokenSession('lip_bobby')
    client = berserk.Client(session, base_url="http://lila:9663")

    assert client.account.get_kid_mode() == False
    client.account.set_kid_mode(True)
    assert client.account.get_kid_mode() == True
