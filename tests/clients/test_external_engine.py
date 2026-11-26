import requests_mock

from berserk import Client

ENGINE_KWARGS = dict(
    name="Test Engine",
    max_threads=4,
    max_hash_table_size=512,
    default_depth=20,
    provider_secret="s" * 16,
)

EXPECTED_ENGINE_BODY = {
    "name": "Test Engine",
    "maxThreads": 4,
    "maxHash": 512,
    "defaultDepth": 20,
    "variants": None,
    "providerSecret": "s" * 16,
    "providerData": None,
}


class TestExternalEngine:
    def test_create_sends_json_body(self):
        with requests_mock.Mocker() as m:
            m.post("https://lichess.org/api/external-engine", json={"id": "eei_x"})
            Client().external_engine.create(**ENGINE_KWARGS)
            assert m.last_request.headers["Content-Type"] == "application/json"
            assert m.last_request.json() == EXPECTED_ENGINE_BODY

    def test_update_sends_json_body(self):
        with requests_mock.Mocker() as m:
            m.put("https://lichess.org/api/external-engine/eei_x", json={"id": "eei_x"})
            Client().external_engine.update("eei_x", **ENGINE_KWARGS)
            assert m.last_request.headers["Content-Type"] == "application/json"
            assert m.last_request.json() == EXPECTED_ENGINE_BODY

    def test_acquire_request_sends_json_body(self):
        with requests_mock.Mocker() as m:
            m.post(
                "https://engine.lichess.ovh/api/external-engine/work",
                json={"id": "work_x"},
            )
            Client().external_engine.acquire_request("s" * 16)
            assert m.last_request.headers["Content-Type"] == "application/json"
            assert m.last_request.json() == {"providerSecret": "s" * 16}

    def test_analyse_sends_json_body_with_only_the_given_limit(self):
        with requests_mock.Mocker() as m:
            m.post(
                "https://engine.lichess.ovh/api/external-engine/eei_x/analyse",
                text='{"time": 1, "depth": 1, "nodes": 1, "pvs": []}\n',
            )
            list(
                Client().external_engine.analyse(
                    "eei_x",
                    client_secret="ees_x",
                    session_id="sess",
                    threads=2,
                    hash_table_size=64,
                    pri_num_variations=1,
                    variant="chess",
                    initial_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                    moves=["e2e4"],
                    depth=20,
                )
            )
            assert m.last_request.headers["Content-Type"] == "application/json"
            # movetime and nodes must be absent, not null: the server expects exactly one limit
            assert m.last_request.json() == {
                "clientSecret": "ees_x",
                "work": {
                    "sessionId": "sess",
                    "threads": 2,
                    "hash": 64,
                    "multiPv": 1,
                    "variant": "chess",
                    "initialFen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                    "moves": ["e2e4"],
                    "depth": 20,
                },
            }
