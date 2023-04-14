# -*- coding: utf-8 -*-
"""External engine-related endpoints."""
from __future__ import annotations

from json import JSONDecoder
from typing import Any, Dict, Iterator, List, Optional, cast

from ..enums import Variant
from ..formats import JSON, JSON_LIST, NDJSON, TEXT
from .base import BaseClient


class ExternalEngine(BaseClient):
    """
    Client for external engine-related endpoints.

    .. warning::
        External engine is in alpha and is subject to change.
    """

    def list_engines(self) -> List[Dict[str, Any]]:
        """List all registered external engines, with credentials.

        :return List[Dict[str, Any]]: External engines list."""
        path: str = "api/external-engine"
        return self._r.get(path, fmt=JSON_LIST)

    def create_engine(
        self,
        name: str,
        max_threads: int,
        max_hash: int,
        default_depth: int,
        provider_secret: str,
        variants: Optional[List[Variant]] = None,
        provider_data: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a new external engine.

        :param str name: display name of the engine
        :param int max_threads: maximum number of available threads
        :param int max_hash: maximum hash table size in MiB
        :param int default_depth: estimated depth of normal search
        :param str provider_secret: a random token to provide analysis
        :param Optional[List[Variant]] variants: supported chess variants
        :param Optional[str] provider_data: arbitrary data for providers
        :return Dict[str, Any]: the registered engine
        """
        path: str = "api/external-engine"
        json: Dict[str, Any] = {
            "name": name,
            "maxThreads": max_threads,
            "maxHash": max_hash,
            "defaultDepth": default_depth,
            "providerSecret": provider_secret,
        }
        if variants:
            json["variant"] = variants
        if provider_data:
            json["providerData"] = provider_data
        return self._r.post(path, json=json)

    def get_engine(self, identifier: str) -> Dict[str, Any]:
        """Get properties and credentials of an external engine.

        :param str identifier: external engine id
        :return Dict[str, Any]: a registered engine
        """
        path: str = f"api/external-engine/{identifier}"
        return self._r.get(path)

    def update_engine(
        self,
        identifier: str,
        name: str,
        max_threads: int,
        max_hash: int,
        default_depth: int,
        provider_secret: str,
        variants: Optional[List[Variant]] = None,
        provider_data: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing external engine.

        :param str identifier: external engine id
        :param str name: display name of the engine
        :param int max_threads: maximum number of available threads
        :param int max_hash: maximum hash table size in MiB
        :param int default_depth: estimated depth of normal search
        :param str provider_secret: a random token to provide analysis
        :param Optional[List[Variant]] variants: supported chess variants
        :param Optional[str] provider_data: arbitrary data for providers
        :return Dict[str, Any]: the registered engine
        """
        path: str = f"api/external-engine/{identifier}"
        json: Dict[str, Any] = {
            "name": name,
            "maxThreads": max_threads,
            "maxHash": max_hash,
            "defaultDepth": default_depth,
            "providerSecret": provider_secret,
        }
        if variants:
            json["variant"] = variants
        if provider_data:
            json["providerData"] = provider_data
        return self._r.request("PUT", path, json=json, fmt=JSON)

    def delete_engine(self, identifier: str) -> bool:
        """Delete an external engine.

        :param str identifier: external engine id
        :return bool: True if successful
        """
        path: str = f"api/external-engine/{identifier}"
        return cast(bool, self._r.request("DELETE", path, fmt=JSON)["ok"])

    def analyse_with_external_engine(
        self,
        identifier: str,
        client_secret: str,
        /,
        session_id: str,
        threads: int,
        hash: int,
        multi_pv: int,
        variant: Variant,
        initial_fen: str,
        moves: list[str],
        infinite: Optional[bool] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Request analysis from an external engine.

        :param str identifier: external engine id
        :param str client_secret: client secret
        :param str session_id: arbitrary, identifies the analysis session
        :param int threads: number of threads used for analysis
        :param int hash: hash table size to use for analysis
        :param int multi_pv: number of principal variations
        :param Variant variant: variant to analyse
        :param str initial_fen: initial position of the game
        :param list[str] moves: list of UCI moves since the initial position
        :param Optional[bool] infinite: search infinite instead of ``default_depth``
        :return Iterator[Dict[str, Any]]: stream of analysis output
        """
        path: str = (
            f"https://engine.lichess.ovh/api/external-engine/{identifier}/analyse"
        )
        json: Dict[str, Any] = {
            "clientSecret": client_secret,
            "work": {
                "sessionId": session_id,
                "threads": threads,
                "hash": hash,
                "multiPv": multi_pv,
                "variant": variant,
                "initialFen": initial_fen,
                "moves": moves,
            },
        }
        if infinite is not None:
            json["infinite"] = infinite
        yield from self._r.post(path, stream=True, json=json, fmt=NDJSON)

    def acquire_analysis_request(self, provider_secret: str) -> Dict[str, Any]:
        """Wait for analysis requests.

        .. note::
            Uses long polling.
            See `API documentation <https://lichess.org/api>`_.

            This function will automatically wait for a job.

        :param str provider_secret: provider secret
        :return Dict[str, Any]: analysis
        """
        path: str = "https://engine.lichess.ovh/api/external-engine/work"
        json: Dict[str, Any] = {"providerSecret": provider_secret}
        answer: str = self._r.post(path, json=json, fmt=TEXT)
        while answer == "":
            answer = self._r.post(path, json=json, fmt=TEXT)
        decoder: JSONDecoder = JSONDecoder()
        return cast(Dict[str, Any], decoder.decode(answer))

    def answer_analysis_request(self, identifier: str, results: str) -> str:
        """Answer an analysis request.

        :param str identifier: analysis id
        :param str results: engine output
        :return str: thanks
        """
        path: str = f"https://engine.lichess.ovh/api/external-engine/work/{identifier}"
        payload: str = results
        return self._r.post(path, data=payload, fmt=TEXT)
