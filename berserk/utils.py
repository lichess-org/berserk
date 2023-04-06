from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, TypeVar, cast

T = TypeVar("T")
U = TypeVar("U")


def to_millis(dt: datetime) -> int:
    """Return the milliseconds between the given datetime and the epoch."""
    return int(dt.timestamp() * 1000)


def datetime_from_seconds(ts: float) -> datetime:
    """Return the datetime for the given seconds since the epoch.

    UTC is assumed. The returned datetime is timezone aware.
    """
    return datetime.fromtimestamp(ts, timezone.utc)


def datetime_from_millis(millis: float) -> datetime:
    """Return the datetime for the given millis since the epoch.

    UTC is assumed. The returned datetime is timezone aware.
    """
    return datetime_from_seconds(millis / 1000)


def datetime_from_str(dt_str: str) -> datetime:
    """Convert the time in a string to a datetime.

    UTC is assumed. The returned datetime is timezone aware. The format
    must match ``%Y-%m-%dT%H:%M:%S.%fZ``.
    """
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=timezone.utc)


def datetime_from_str_or_millis(millis_or_str: str | int) -> datetime:
    """Convert a string or int to a datetime.

    UTC is assumed. The returned datetime is timezone aware.
    If the input is a string, the format must match ``%Y-%m-%dT%H:%M:%S.%fZ``.
    """
    if isinstance(millis_or_str, int):
        return datetime_from_millis(millis_or_str)
    return datetime_from_str(millis_or_str)


class RatingHistoryEntry(NamedTuple):
    year: int
    month: int
    day: int
    rating: int


def rating_history(data: Tuple[int, int, int, int]):
    return RatingHistoryEntry(*data)


def inner(
    func: Callable[[T], U], *keys: str
) -> Callable[[Dict[str, T]], Dict[str, T | U]]:
    def convert(data: Dict[str, T]) -> Dict[str, T | U]:
        result = cast(Dict[str, T | U], data)
        for k in keys:
            try:
                result[k] = func(data[k])
            except KeyError:
                pass  # normal for keys to not be present sometimes
        return result

    return convert


def listing(func: Callable[[T], U]) -> Callable[[List[T]], List[U]]:
    def convert(items: List[T]):
        return [func(item) for item in items]

    return convert


def noop(arg: T) -> T:
    return arg


def build_adapter(mapper: Dict[str, str], sep: str = "."):
    """Build a data adapter.

    Uses a map to pull values from an object and assign them to keys.
    For example:

    .. code-block:: python

        >>> mapping = {
        ...   'broadcast_id': 'broadcast.id',
        ...   'slug': 'broadcast.slug',
        ...   'name': 'broadcast.name',
        ...   'description': 'broadcast.description',
        ...   'syncUrl': 'broadcast.sync.url',
        ... }

        >>> cast = {'broadcast': {'id': 'WxOb8OUT',
        ...   'slug': 'test-tourney',
        ...   'name': 'Test Tourney',
        ...   'description': 'Just a test',
        ...   'ownerId': 'rhgrant10',
        ...   'sync': {'ongoing': False, 'log': [], 'url': None}},
        ...  'url': 'https://lichess.org/broadcast/test-tourney/WxOb8OUT'}

        >>> adapt = build_adapter(mapping)
        >>> adapt(cast)
        {'broadcast_id': 'WxOb8OUT',
        'slug': 'test-tourney',
        'name': 'Test Tourney',
        'description': 'Just a test',
        'syncUrl': None}

    :param dict mapper: map of keys to their location in an object
    :param str sep: nested key delimiter
    :return: adapted data
    :rtype: dict
    """

    def get(data: Dict[str, Any], location: str) -> Dict[str, Any]:
        for key in location.split(sep):
            data = data[key]
        return data

    def adapter(
        data: Dict[str, Any], default: Any = None, fill: bool = False
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, loc in mapper.items():
            try:
                result[key] = get(data, loc)
            except KeyError:
                if fill:
                    result[key] = default
        return result

    return adapter
