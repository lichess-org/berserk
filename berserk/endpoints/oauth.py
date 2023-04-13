# -*- coding: utf-8 -*-
"""OAuth-related endpoints."""
from .. import models
from . import BaseClient


class OAuth(BaseClient):
    """Client for OAuth-related endpoints."""

    def test_tokens(self, *tokens):
        """Test the validity of up to 1000 OAuth tokens

        Valid OAuth tokens will be returned with their
        associated user ID and scopes. Invalid tokens
        will be returned as null.

        :param tokens: one or more OAuth tokens
        :return: list
        """
        path = "api/token/test"
        payload = ",".join(tokens)
        return self._r.post(path, data=payload, converter=models.OAuth.convert)
