from urllib.parse import parse_qs

import requests_mock

from berserk import Client


class TestBulkPairings:
    def test_create_sends_form_body(self):
        with requests_mock.Mocker() as m:
            m.post("https://lichess.org/api/bulk-pairing", json={"id": "bp_x"})
            Client().bulk_pairings.create(
                [("tokenA", "tokenB"), ("tokenC", "tokenD")],
                clock_limit=300,
                clock_increment=2,
            )
            assert (
                m.last_request.headers["Content-Type"]
                == "application/x-www-form-urlencoded"
            )
            # unset (None) fields are omitted; booleans must be lowercase for the server
            assert parse_qs(m.last_request.text) == {
                "players": ["tokenA:tokenB,tokenC:tokenD"],
                "clock.limit": ["300"],
                "clock.increment": ["2"],
                "rated": ["false"],
            }
