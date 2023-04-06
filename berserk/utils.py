import collections
from datetime import datetime, timezone


def to_millis(dt):
    """Return the milliseconds between the given datetime and the epoch.

    :param datetime dt: a datetime
    :return: milliseconds since the epoch
    :rtype: int
    """
    return int(dt.timestamp() * 1000)


def datetime_from_seconds(ts):
    """Return the datetime for the given seconds since the epoch.

    UTC is assumed. The returned datetime is timezone aware.

    :return: timezone aware datetime
    :rtype: :class:`datetime`
    """
    return datetime.fromtimestamp(ts, timezone.utc)


def datetime_from_millis(millis):
    """Return the datetime for the given millis since the epoch.

    UTC is assumed. The returned datetime is timezone aware.

    :return: timezone aware datetime
    :rtype: :class:`datetime`
    """
    return datetime_from_seconds(millis / 1000)


def datetime_from_str(dt_str):
    """Convert the time in a string to a datetime.

    UTC is assumed. The returned datetime is timezone aware. The format
    must match ``%Y-%m-%dT%H:%M:%S.%fZ``.

    :return: timezone aware datetime
    :rtype: :class:`datetime`
    """
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=timezone.utc)


_RatingHistoryEntry = collections.namedtuple("Entry", "year month day rating")


def rating_history(data):
    return _RatingHistoryEntry(*data)


def inner(func, *keys):
    def convert(data):
        for k in keys:
            try:
                data[k] = func(data[k])
            except KeyError:
                pass  # normal for keys to not be present sometimes
        return data

    return convert


def listing(func):
    def convert(items):
        result = []
        for item in items:
            result.append(func(item))
        return result

    return convert


def noop(arg):
    return arg


def build_adapter(mapper, sep="."):
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

    def get(data, location):
        for key in location.split(sep):
            data = data[key]
        return data

    def adapter(data, default=None, fill=False):
        result = {}
        for key, loc in mapper.items():
            try:
                result[key] = get(data, loc)
            except KeyError:
                if fill:
                    result[key] = default
        return result

    return adapter
