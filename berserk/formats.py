from __future__ import annotations
import json
from typing import Any, Callable, Dict, Generic, Iterator, List, Type, TypeVar, cast

import ndjson  # type: ignore
from requests import Response

from . import utils

T = TypeVar("T")


class FormatHandler(Generic[T]):
    """Provide request headers and parse responses for a particular format.

    Instances of this class should override the :meth:`parse_stream` and
    :meth:`parse` methods to support handling both streaming and non-streaming
    responses.

    :param mime_type: the MIME type for the format
    """

    def __init__(self, mime_type: str):
        self.mime_type = mime_type
        self.headers = {"Accept": mime_type}

    def handle(
        self,
        response: Response,
        is_stream: bool,
        converter: Callable[[T], T] = utils.noop,
    ) -> T | Iterator[T]:
        """Handle the response by returning the data.

        :param response: raw response
        :type response: :class:`requests.Response`
        :param bool is_stream: ``True`` if the response is a stream
        :param func converter: function to handle field conversions
        :return: either all response data or an iterator of response data
        """
        if is_stream:
            return map(converter, iter(self.parse_stream(response)))
        else:
            return converter(self.parse(response))

    def parse(self, response: Response) -> T:
        """Parse all data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        """
        raise NotImplementedError

    def parse_stream(self, response: Response) -> Iterator[T]:
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over the response data
        """
        raise NotImplementedError


class JsonHandler(FormatHandler[Dict[str, Any]]):
    """Handle JSON data.

    :param str mime_type: the MIME type for the format
    :param decoder: the decoder to use for the JSON format
    :type decoder: :class:`json.JSONDecoder`
    """

    def __init__(
        self, mime_type: str, decoder: Type[json.JSONDecoder] = json.JSONDecoder
    ):
        super().__init__(mime_type=mime_type)
        self.decoder = decoder

    def parse(self, response: Response) -> Dict[str, Any]:
        """Parse all JSON data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        :rtype: JSON
        """
        return response.json(cls=self.decoder)

    def parse_stream(self, response: Response) -> Iterator[Dict[str, Any]]:
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple JSON objects
        """
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                yield json.loads(decoded_line)


class PgnHandler(FormatHandler[str]):
    """Handle PGN data."""

    def __init__(self):
        super().__init__(mime_type="application/x-chess-pgn")

    def parse(self, response: Response) -> str:
        """Parse all text data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response text
        :rtype: str
        """
        return response.text

    def parse_stream(self, response: Response) -> Iterator[str]:
        """Yield the parsed PGN games from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple PGN texts
        """
        lines: List[str] = []
        last_line = True
        for line in response.iter_lines():
            decoded_line = line.decode("utf-8")
            if last_line or decoded_line:
                lines.append(decoded_line)
            else:
                yield "\n".join(lines).strip()
                lines = []
            last_line = decoded_line

        if lines:
            yield "\n".join(lines).strip()


class TextHandler(FormatHandler[str]):
    def __init__(self):
        super().__init__(mime_type="text/plain")

    def parse(self, response: Response) -> str:
        return response.text

    def parse_stream(self, response: Response) -> Iterator[str]:
        yield from response.iter_lines()


#: Basic text
TEXT = TextHandler()

#: Handles vanilla JSON
JSON = JsonHandler(mime_type="application/json")

#: Handle vanilla JSON where the response is a top-level list (this is only needed bc of type checking)
JSON_LIST = cast(FormatHandler[List[Dict[str, Any]]], JSON)

#: Handles oddball LiChess JSON (normal JSON, crazy MIME type)
LIJSON = JsonHandler(mime_type="application/vnd.lichess.v3+json")

#: Handles newline-delimited JSON
NDJSON = JsonHandler(mime_type="application/x-ndjson", decoder=ndjson.Decoder)  # type: ignore

#: Handles newline-delimited JSON where the response is a top-level list (this is only needed bc of type checking,
# if not streaming NDJSON, the result is always a list)
NDJSON_LIST = cast(FormatHandler[List[Dict[str, Any]]], NDJSON)

#: Handles PGN
PGN = PgnHandler()
