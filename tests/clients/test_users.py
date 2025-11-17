import pytest

from berserk import Client, OnlineLightUser
from typing import List
from utils import validate, skip_if_older_3_dot_10


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_autocomplete_as_object(self):
        res = Client().users.get_by_autocomplete("thisisatest", as_object=True)
        validate(List[OnlineLightUser], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_autocomplete(self):
        res = Client().users.get_by_autocomplete("thisisatest")
        validate(List[str], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_autocomplete_not_found(self):
        res = Client().users.get_by_autocomplete("username_not_found__")
        validate(List[str], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_autocomplete_as_object_not_found(self):
        res = Client().users.get_by_autocomplete("username_not_found__", as_object=True)
        validate(List[OnlineLightUser], res)
