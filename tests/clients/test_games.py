import pytest
import berserk
from utils import validate, skip_if_older_3_dot_10

BASE_URL = "http://localhost:9663"
API_TOKEN = "add_your_token"


class TestGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_export_imported_games(self):
        session = berserk.TokenSession(API_TOKEN)  # Add your own
        client = berserk.Client(session, base_url=BASE_URL)
        res = client.games.export_imported()
        validate(str, res)
