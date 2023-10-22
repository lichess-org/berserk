from __future__ import annotations

import base64
import hashlib
import os
import re
import uuid
from typing import Any, Dict

import requests.cookies

from .. import models
from .base import BaseClient


class OAuth(BaseClient):
    def get_code(
        self,
        client_id: str,
        redirect_uri: str,
        scope: str | None = None,
        username: str | None = None,
    ) -> Dict[str, Any]:
        """OAuth2 authorization endpoint.

        :param client_id: arbitrary identifier that uniquely identifies your application
        :param redirect_uri: absolute URL that user should be redirected to with the authorization result
        :param scope: space separated list of OAuth scopes, if any
        :param username: hint to the user to log in with a specific Lichess username
        """
        path = "/oauth"
        state = str(uuid.uuid4())

        # Generate code_verifier for PKCE workflow
        # Source: https://aps.autodesk.com/en/docs/oauth/v2/tutorials/code-challenge/
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
        code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")

        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
            "scope": scope,
            "username": username,
            "state": state,
        }

        # Store code_verifier in session storage
        self._r.session.cookies.clear_session_cookies()
        self._r.session.cookies.set(name="code_verifier", value=code_verifier)
        response = self._r.get(path=path, params=params)

        # To defend against cross-site request forgery, check that the returned state matches the original state
        if returned_state := response.get("state"):
            if state == returned_state:
                return response
            else:
                return {
                    "error": "unexpected_state",
                    "error_description": "potential cross-site request forgery",
                    "state": "returned_state",
                }

        return response

    def get_token(self, code: str, redirect_uri: str, client_id: str) -> Dict[str, str]:
        """Exchanges an authorization code for an access token.

        :param code: authorization code that was sent in code parameter to the redirect URI
        :param redirect_uri: must match redirect URL used to request the authorization code
        :param client_id: must match client ID used to request the authorization code
        :return: info about the token
        """
        path = "/api/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": self._r.session.cookies.get("code_verifier"),
            "redirect_uri": redirect_uri,
            "client_id": client_id,
        }
        return self._r.post(path=path, payload=payload)

    def revoke_token(self) -> None:
        """Revokes the access token sent as Bearer for this request"""

        path = "/api/token"
        self._r.request("DELETE", path)

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
