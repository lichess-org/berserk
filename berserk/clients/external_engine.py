from __future__ import annotations

from typing import List, cast, Iterator

from .base import BaseClient
import requests
from ..formats import NDJSON, TEXT
from ..types.common import UciVariant
from ..types.external_engine import ExternalEngineRequest, EngineAnalysisOutput

EXTERNAL_ENGINE_URL = "https://engine.lichess.ovh"


class ExternalEngine(BaseClient):
    """Client for external engine related endpoints."""

    def __init__(
        self,
        session: requests.Session,
        *,
        base_url: str | None = None,
        external_engine_url: str | None = None,
    ):
        """Create a subclient for the endpoints that use a different base url."""
        super().__init__(session, base_url)
        self._external_client = BaseClient(
            session, external_engine_url or EXTERNAL_ENGINE_URL
        )

    def get(self) -> List[ExternalEngine]:
        """Lists all external engines that have been registered for the user, and the credentials required to use them.

        Requires OAuth2 authorization.

        :return: info about the external engines
        """
        path = "/api/external-engine"
        return cast(List[ExternalEngine], self._r.get(path))

    def get_by_id(self, engine_id: str) -> ExternalEngine:
        """Get properties and credentials of an external engine.

        Requires OAuth2 authorization.

        :param engine_id: external engine ID
        :return: info about the external engine
        """
        path = f"/api/external-engine/{engine_id}"
        return cast(ExternalEngine, self._r.get(path))

    def create(
        self,
        name: str,
        max_threads: int,
        max_hash_table_size: int,
        default_depth: int,
        provider_secret: str,
        variants: List[str] | None = None,
        provider_data: str | None = None,
    ) -> ExternalEngine:
        """Registers a new external engine for the user.

        Requires OAuth2 authorization.

        :param name: engine display name
        :param max_threads: maximum number of available threads
        :param max_hash_table_size: maximum available hash table size, in MiB
        :param default_depth: estimated depth of normal search
        :param provider_secret: random token that used to wait for analysis requests and provide analysis
        :param variants: list of supported chess variants
        :param provider_data: arbitrary data that engine provider can use for identification or bookkeeping
        :return: info about the external engine
        """
        path = "/api/external-engine"
        payload = {
            "name": name,
            "maxThreads": max_threads,
            "maxHash": max_hash_table_size,
            "defaultDepth": default_depth,
            "variants": variants,
            "providerSecret": provider_secret,
            "providerData": provider_data,
        }
        return cast(ExternalEngine, self._r.post(path=path, payload=payload))

    def update(
        self,
        engine_id: str,
        name: str,
        max_threads: int,
        max_hash_table_size: int,
        default_depth: int,
        provider_secret: str,
        variants: List[str] | None = None,
        provider_data: str | None = None,
    ) -> ExternalEngine:
        """Updates the properties of an external engine.

        Requires OAuth2 authorization.

        :param engine_id: engine ID
        :param name: engine display name
        :param max_threads: maximum number of available threads
        :param max_hash_table_size: maximum available hash table size, in MiB
        :param default_depth: estimated depth of normal search
        :param provider_secret: random token that used to wait for analysis requests and provide analysis
        :param variants: list of supported chess variants
        :param provider_data: arbitrary data that engine provider can use for identification or bookkeeping
        :return: info about the external engine
        """
        path = f"/api/external-engine/{engine_id}"
        payload = {
            "name": name,
            "maxThreads": max_threads,
            "maxHash": max_hash_table_size,
            "defaultDepth": default_depth,
            "variants": variants,
            "providerSecret": provider_secret,
            "providerData": provider_data,
        }
        return cast(
            ExternalEngine, self._r.request(method="PUT", path=path, payload=payload)
        )

    def delete(self, engine_id: str) -> None:
        """Unregisters an external engine.

        Requires OAuth2 authorization.

        :param engine_id: engine ID
        """
        path = f"/api/external-engine/{engine_id}"
        self._r.request("DELETE", path)

    def analyse(
        self,
        engine_id: str,
        client_secret: str,
        session_id: str,
        threads: int,
        hash_table_size: int,
        pri_num_variations: int,
        variant: UciVariant,
        initial_fen: str,
        moves: List[str],
        movetime: int | None = None,
        depth: int | None = None,
        nodes: int | None = None,
    ) -> Iterator[EngineAnalysisOutput]:
        """
        Analyse with external engine

        Request analysis from an external engine. Response content is streamed as newline delimited JSON.
        The properties are based on the UCI specification.
        Analysis stops when the client goes away, the requested limit is reached, or the provider goes away.

        :param engine_id: external engine id
        :param client_secret: engine credentials
        :param session_id: Arbitary string that identifies the analysis session. Providers may wish to clear the hash table between sessions.
        :param threads: Number of threads to use for analysis.
        :param hash_table_size: Hash table size to use for analysis, in MiB.
        :param pri_num_variations: Requested number of principal variations. (1-5)
        :param variant: uci variant
        :param initial_fen: Initial position of the game.
        :param moves: List of moves played from the initial position, in UCI notation.
        :param movetime: Amount of time to analyse the position, in milliseconds.
        :param depth: Analysis target depth
        :param nodes: Number of nodes to analyse in the position
        """
        path = f"/api/external-engine/{engine_id}/analyse"
        payload = {
            "clientSecret": client_secret,
            "work": {
                "sessionId": session_id,
                "threads": threads,
                "hash": hash_table_size,
                "multiPv": pri_num_variations,
                "variant": variant,
                "initialFen": initial_fen,
                "moves": moves,
                "movetime": movetime,
                "depth": depth,
                "nodes": nodes,
            },
        }

        for response in self._external_client._r.post(
            path=path,
            payload=payload,
            stream=True,
            fmt=NDJSON,
        ):
            yield cast(EngineAnalysisOutput, response)

    def acquire_request(self, provider_secret: str) -> ExternalEngineRequest:
        """Wait for an analysis request to any of the external engines that have been registered with the given secret.
        :param provider_secret: provider credentials
        :return: the requested analysis
        """
        path = "/api/external-engine/work"
        payload = {"providerSecret": provider_secret}
        return cast(
            ExternalEngineRequest,
            self._external_client._r.post(path=path, payload=payload),
        )

    def answer_request(self, engine_id: str) -> str:
        """Submit a stream of analysis as UCI output.
        The server may close the connection at any time, indicating that the requester has gone away and analysis
        should be stopped.
        :param engine_id: engine ID
        :return: the requested analysis
        """
        path = f"/api/external-engine/work/{engine_id}"
        return self._external_client._r.post(path=path, fmt=TEXT)
