from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseClient


class ExternalEngine(BaseClient):
    def get(self) -> Dict[str, Any]:
        """Lists all external engines that have been registered for the user, and the credentials required to use them.

        :return: info about the external engines
        """
        path = "/api/external-engine"
        return self._r.get(path)

    def get_by_id(self, engine_id: str) -> Dict[str, Any]:
        """Get properties and credentials of an external engine.

        :param engine_id: external engine ID
        :return: info about the external engine
        """
        path = f"/api/external-engine/{engine_id}"
        return self._r.get(path)

    def create(
        self,
        name: str,
        max_threads: int,
        max_hash_table_size: int,
        default_depth: int,
        provider_secret: str,
        variants: List[str] | None = None,
        provider_data: str | None = None,
    ) -> Dict[str, Any]:
        """Registers a new external engine for the user.

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
        return self._r.post(path=path, payload=payload)

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
    ) -> Dict[str, Any]:
        """Updates the properties of an external engine.

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
        return self._r.put(path=path, payload=payload)

    def delete(self, engine_id: str) -> None:
        """Unregisters an external engine.

        :param engine_id: engine ID
        """
        path = f"/api/external-engine/{engine_id}"
        self._r.request("DELETE", path)
