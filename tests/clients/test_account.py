import pytest
from datetime import datetime, timezone, timedelta
import berserk
from berserk.utils import to_millis
from berserk.types.account import Timeline
from utils import validate, skip_if_older_3_dot_10

BASE_URL = "http://localhost:9663"


class TestAccount:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_timeline(self):
        session = berserk.TokenSession("API_TOKEN")  # Add your own
        client = berserk.Client(session, base_url=BASE_URL)
        since = datetime.now(timezone.utc) - timedelta(days=14)
        nb = 15
        res = client.account.get_timeline(since=to_millis(since), nb=nb)
        validate(Timeline, res)
