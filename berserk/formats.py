import json

import ndjson

from . import utils


class FormatHandler:
    """Provide request headers and parse responses for a particular format.

    Instances of this class should override the :meth:`parse_stream` and
    :meth:`parse` methods to support handling both streaming and non-streaming
    responses.

    :param str mime_type: the MIME type for the format
    """

    def __init__(self, mime_type):
        self.mime_type = mime_type
        self.headers = {"Accept": mime_type}

    def handle(self, response, is_stream, converter=utils.noop):
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

    def parse(self, response):
        """Parse all data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        """
        return response

    def parse_stream(self, response):
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over the response data
        """
        yield response


class JsonHandler(FormatHandler):
    """Handle JSON data.

    :param str mime_type: the MIME type for the format
    :param decoder: the decoder to use for the JSON format
    :type decoder: :class:`json.JSONDecoder`
    """

    def __init__(self, mime_type, decoder=json.JSONDecoder):
        super().__init__(mime_type=mime_type)
        self.decoder = decoder

    def parse(self, response):
        """Parse all JSON data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        :rtype: JSON
        """
        return response.json(cls=self.decoder)

    def parse_stream(self, response):
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple JSON objects
        """
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                yield json.loads(decoded_line)


class PgnHandler(FormatHandler):
    """Handle PGN data."""

    def __init__(self):
        super().__init__(mime_type="application/x-chess-pgn")

    def handle(self, *args, **kwargs):
        kwargs["converter"] = utils.noop  # disable conversions
        return super().handle(*args, **kwargs)

    def parse(self, response):
        """Parse all text data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response text
        :rtype: str
        """
        return response.text

    def parse_stream(self, response):
        """Yield the parsed PGN games from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple PGN texts
        """
        lines = []
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


class TextHandler(FormatHandler):
    def __init__(self):
        super().__init__(mime_type="text/plain")

    def parse(self, response):
        return response.text

    def parse_stream(self, response):
        yield from response.iter_lines()


#: Basic text
TEXT = TextHandler()

#: Handles vanilla JSON
JSON = JsonHandler(mime_type="application/json")

#: Handles oddball LiChess JSON (normal JSON, crazy MIME type)
LIJSON = JsonHandler(mime_type="application/vnd.lichess.v3+json")

#: Handles newline-delimited JSON
NDJSON = JsonHandler(mime_type="application/x-ndjson", decoder=ndjson.Decoder)

#: Handles PGN
PGN = PgnHandler()
