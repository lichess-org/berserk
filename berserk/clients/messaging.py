from __future__ import annotations

from .base import BaseClient


class Messaging(BaseClient):
    def send(self, username: str, text: str) -> None:
        """Send a private message to another player.

        :param username: the user to send the message to
        :param text: the text to send
        """
        path = f"/inbox/{username}"
        payload = {"text": text}
        self._r.post(path, data=payload)
