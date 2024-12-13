import pytest
import requests_mock

from berserk import Client, PaginatedTopBroadcasts
from utils import validate, skip_if_older_3_dot_10

import requests_mock
from typing import List, Dict
from berserk.types.broadcast import (
    BroadcastWithLastRound,
    BroadcastPaginationMetadata,
    BroadcastByUser,
)


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


class TestResetBroadcastRound:
    def test_broadcast_round_id_param(self):
        """The test verifies that the broadcast round id parameter is passed correctly in the query params."""
        with requests_mock.Mocker() as m:
            broadcast_round_id = "12345678"
            m.post(
                f"https://lichess.org/api/broadcast/round/{broadcast_round_id}/reset",
                json={"ok": True},
            )
            res = Client().broadcasts.reset_round(broadcast_round_id=broadcast_round_id)


class TestBroadcastByUsername:
    # test complete response
    @skip_if_older_3_dot_10
    def test_response_type_total(self):
        """Verify that the response matches the total model"""
        res = Client().broadcasts.get_by_user(username="STL_Carlsen", html=True, page=1)
        validate(BroadcastByUser, res)

    def test_broadcast_round_id_param(self):
        """The test verifies that the username parameter is passed correctly in the query params."""
        with requests_mock.Mocker() as m:
            username = "STL_Carlsen"
            m.get(
                f"https://lichess.org/api/broadcast/by/{username}",
                json={"ok": True},
            )
            res = Client().broadcasts.get_by_user(username=username, html=False, page=1)
