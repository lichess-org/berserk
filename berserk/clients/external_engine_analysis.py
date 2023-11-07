from typing import List, Iterator, cast, Optional

import requests

from .base import BaseClient
from ..formats import NDJSON, TEXT
from ..types.external_engine import ExternalEngineRequest, EngineAnalysisOutput

ENGINE_URL = "https://engine.lichess.ovh"


class ExternalEngineAnalysis(BaseClient):
    """Client for external engine analysis related endpoints."""

    def __init__(self, session: requests.Session, engine_url: Optional[str] = None):
        super().__init__(session, engine_url or ENGINE_URL)

    def analyse(
        self,
        engine_id: str,
        client_secret: str,
        session_id: str,
        threads: int,
        hash_table_size: int,
        num_variations: int,
        variant: str,
        initial_fen: str,
        moves: List[str],
        infinite: Optional[bool] = None,
    ) -> Iterator[EngineAnalysisOutput]:
        """Request analysis from an external engine.

        Response content is streamed as newline delimited JSON. The properties are based on the UCI specification.
        Analysis stops when the client goes away, the requested limit is reached, or the provider goes away.

        :param engine_id: engine ID
        :param client_secret: engine credentials
        :param session_id: arbitrary string that identifies the analysis session
        :param threads: number of threads to use for analysis
        :param hash_table_size: hash table size to use for analysis, in MiB
        :param num_variations: requested number of principle variation
        :param variant: chess UCI variant
        :param initial_fen: initial position of the game
        :param moves: list of moves played from the initial position, in UCI notation
        :param infinite: request an infinite search (rather than roughly aiming for defaultDepth)
        :return: iterator over the request analysis from the external engine
        """
        path = f"/api/external-engine/{engine_id}/analyse"
        payload = {
            "clientSecret": client_secret,
            "work": {
                "sessionId": session_id,
                "threads": threads,
                "hash": hash_table_size,
                "infinite": infinite,
                "multiPv": num_variations,
                "variant": variant,
                "initialFen": initial_fen,
                "moves": moves,
            },
        }
        yield from self._r.post(path=path, payload=payload, stream=True, fmt=NDJSON)

    def acquire_request(self, provider_secret: str) -> ExternalEngineRequest:
        """Wait for an analysis request to any of the external engines that have been registered with the given secret.

        :param provider_secret: provider credentials
        :return: the requested analysis
        """
        path = "/api/external-engine/work"
        payload = {"providerSecret": provider_secret}
        return cast(ExternalEngineRequest, self._r.post(path=path, payload=payload))

    def answer_request(self, engine_id: str) -> str:
        """Submit a stream of analysis as UCI output.

        The server may close the connection at any time, indicating that the requester has gone away and analysis
        should be stopped.

        :param engine_id: engine ID
        :return: the requested analysis
        """
        path = f"/api/external-engine/work/{engine_id}"
        return self._r.post(path=path, fmt=TEXT)
