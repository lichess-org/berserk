from __future__ import annotations

from typing import Any, Dict

from .. import models
from .base import BaseClient


class OAuth(BaseClient):
    def test_tokens(self, *tokens: str) -> Dict[str, Any]:
        """Test the validity of up to 1000 OAuth tokens.

        Valid OAuth tokens will be returned with their associated user ID and scopes.
        Invalid tokens will be returned as null.

        :param tokens: one or more OAuth tokens
        :return: info about the tokens
        """
        path = "/api/token/test"
        payload = ",".join(tokens)
        return self._r.post(path, data=payload, converter=models.OAuth.convert)
