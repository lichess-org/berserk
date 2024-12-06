from __future__ import annotations
import logging
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    Literal,
    Mapping,
    TypeVar,
    Union,
    overload,
)
from urllib.parse import urljoin

import requests

from berserk.formats import FormatHandler

from . import exceptions, utils

LOG = logging.getLogger(__name__)

T = TypeVar("T")
U = TypeVar("U")

Params = Mapping[str, Union[int, bool, str, None]]
Data = Union[str, Params]
Converter = Callable[[T], T]


class Requestor(Generic[T]):
    """Encapsulates the logic for making a request.

    :param session: the authenticated session object
    :param str base_url: the base URL for requests
    :param default_fmt: default format handler to use
    """

    def __init__(
        self, session: requests.Session, base_url: str, default_fmt: FormatHandler[T]
    ):
        self.session = session
        self.base_url = base_url
        self.default_fmt = default_fmt

    def request(
        self,
        method: str,
        path: str,
        *,
        stream: bool = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[Any] | None = None,
        converter: Converter[Any] = utils.noop,
        **kwargs: Any,
    ) -> Any | Iterator[Any]:
        """Make a request for a resource in a particular format.

        :param method: HTTP verb
        :param path: the URL suffix
        :param stream: whether to stream the response
        :param params: request query parameters
        :param data: request body data (url-encoded)
        :param json: request body json
        :param fmt: the format handler
        :param converter: function to handle field conversions
        :return: response
        :raises berserk.exceptions.ResponseError: if the status is >=400
        """
        fmt = fmt or self.default_fmt
        url = urljoin(self.base_url, path)

        LOG.debug(
            "%s %s %s params=%s data=%s json=%s",
            "stream" if stream else "request",
            method,
            url,
            params,
            data,
            json,
        )
        try:
            response = self.session.request(
                method,
                url,
                stream=stream,
                params=params,
                headers=fmt.headers,
                data=data,
                json=json,
                **kwargs,
            )
        except requests.RequestException as e:
            raise exceptions.ApiError(e)
        if not response.ok:
            raise exceptions.ResponseError(response)

        return fmt.handle(response, is_stream=stream, converter=converter)

    @overload
    def get(
        self,
        path: str,
        *,
        stream: Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[U],
        converter: Converter[U] = utils.noop,
        **kwargs: Any,
    ) -> U:
        ...

    @overload
    def get(
        self,
        path: str,
        *,
        stream: Literal[True],
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[U],
        converter: Converter[U] = utils.noop,
        **kwargs: Any,
    ) -> Iterator[U]:
        ...

    @overload
    def get(
        self,
        path: str,
        *,
        stream: Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: None = None,
        converter: Converter[T] = utils.noop,
        **kwargs: Any,
    ) -> T:
        ...

    @overload
    def get(
        self,
        path: str,
        *,
        stream: Literal[True],
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: None = None,
        converter: Converter[T] = utils.noop,
        **kwargs: Any,
    ) -> Iterator[T]:
        ...

    def get(
        self,
        path: str,
        *,
        stream: Literal[True] | Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[Any] | None = None,
        converter: Any = utils.noop,
        **kwargs: Any,
    ) -> Any | Iterator[Any]:
        """Convenience method to make a GET request."""
        return self.request(
            "GET",
            path,
            params=params,
            stream=stream,
            fmt=fmt,
            converter=converter,
            data=data,
            json=json,
            **kwargs,
        )

    @overload
    def post(
        self,
        path: str,
        *,
        stream: Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[U],
        converter: Converter[U] = utils.noop,
        **kwargs: Any,
    ) -> U:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        stream: Literal[True],
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[U],
        converter: Converter[U] = utils.noop,
        **kwargs: Any,
    ) -> Iterator[U]:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        stream: Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: None = None,
        converter: Converter[T] = utils.noop,
        **kwargs: Any,
    ) -> T:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        stream: Literal[True],
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: None = None,
        converter: Converter[T] = utils.noop,
        **kwargs: Any,
    ) -> Iterator[T]:
        ...

    def post(
        self,
        path: str,
        *,
        stream: Literal[True] | Literal[False] = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[Any] | None = None,
        converter: Any = utils.noop,
        **kwargs: Any,
    ) -> Any | Iterator[Any]:
        """Convenience method to make a POST request."""
        return self.request(
            "POST",
            path,
            params=params,
            stream=stream,
            fmt=fmt,
            converter=converter,
            data=data,
            json=json,
            **kwargs,
        )


class TokenSession(requests.Session):
    """Session capable of personal API token authentication.

    :param token: personal API token
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
