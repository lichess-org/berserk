import requests_mock

import berserk


class TestTableBaseUrl:
    def test_default(self):
        client = berserk.Client()
        with requests_mock.Mocker() as m:
            m.get("https://tablebase.lichess.ovh/standard", json={})
            client.tablebase.look_up("4k3/6KP/8/8/8/8/7p/8_w_-_-_0_1")

    def test_overight_url(self):
        client = berserk.Client(tablebase_url="https://my-tablebase.com")
        with requests_mock.Mocker() as m:
            m.get("https://my-tablebase.com/standard", json={})
            client.tablebase.look_up("4k3/6KP/8/8/8/8/7p/8_w_-_-_0_1")
