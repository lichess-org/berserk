# -*- coding: utf-8 -*-
"""Messaging-related endpoints."""
from . import BaseClient


class Messaging(BaseClient):
    """Client for messaging-related endpoints."""

    def send(self, username: str, text: str):
        """Send a private message to another player.

        :param str username: the user to send the message to
        :param str text: the text to send
        """
        path = f"/inbox/{username}"
        payload = {"text": text}
        self._r.post(path, data=payload)
