import pytest

from berserk import Client, TokenSession
from berserk.types import ChallengeJson
from utils import skip_if_older_3_dot_10, validate


class TestChallenges:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_show(self):
        res = Client(session=TokenSession("fake-token")).challenges.show("testChallenge1")
        validate(ChallengeJson, res)
