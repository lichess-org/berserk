import pytest

from berserk import Client
from berserk.types.broadcast import BroadcastTopResponse
from utils import skip_if_older_3_dot_10, validate


class TestBroadcasts:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_top(self):
        res = Client().broadcasts.get_top(page=1, html=False)
        validate(BroadcastTopResponse, res)
