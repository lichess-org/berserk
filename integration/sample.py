import berserk

session = berserk.TokenSession('lip_bobby')
client = berserk.Client(session, base_url="http://lila:9663")

me = client.account.get()
assert me['id'] == 'bobby'

assert client.account.get_email() == 'bobby@localhost'

assert client.account.get_kid_mode() == False
client.account.set_kid_mode(True)
assert client.account.get_kid_mode() == True
