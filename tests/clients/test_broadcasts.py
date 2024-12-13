import pytest
import requests_mock

from berserk import Client, PaginatedTopBroadcasts
from utils import validate, skip_if_older_3_dot_10


from typing import List, Dict
from berserk.types.broadcast import BroadcastWithLastRound, BroadcastPaginationMetadata


class TestTopBroadcasts:
    # test complete response
    @skip_if_older_3_dot_10
    def test_response_type_total(self):
        """Verify that the response matches the total model"""
        res = Client().broadcasts.get_top(html=True, page=1)
        validate(PaginatedTopBroadcasts, res)

    # In the following we test the subparts of the response.
    # This makes it easier to locate errors.

    # test response['active']
    @skip_if_older_3_dot_10
    def test_response_type_active_model(self):
        """Verify that the response matches the typed-dict"""
        res = Client().broadcasts.get_top(html=True, page=1)
        validate(List[BroadcastWithLastRound], res.get("active", []))

    # test response['past']
    @skip_if_older_3_dot_10
    def test_response_type_past_model(self):
        """Verify that the response matches the typed-dict"""
        res = Client().broadcasts.get_top(html=True, page=1)
        validate(BroadcastPaginationMetadata, res.get("past", []))

    # test response['upcoming']
    @skip_if_older_3_dot_10
    def test_response_type_upcoming_model(self):
        """Verify that the response matches the typed-dict"""
        res = Client().broadcasts.get_top(html=True, page=1)
        validate(List[BroadcastWithLastRound], res.get("upcoming", []))
