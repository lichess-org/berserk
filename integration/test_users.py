import berserk

def test_account_get():
    client = berserk.Client(base_url="http://lila:9663")

    top_10 = client.users.get_all_top_10()
    
    assert len(top_10['bullet']) == 10
