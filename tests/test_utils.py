import datetime
import collections
import pytest

from berserk import utils

Case = collections.namedtuple("Case", "dt seconds millis text")


@pytest.fixture
def time_case():
    dt = datetime.datetime(2017, 12, 28, 23, 52, 30, tzinfo=datetime.timezone.utc)
    ts = dt.timestamp()
    return Case(dt, ts, ts * 1000, dt.isoformat())


def test_to_millis(time_case):
    assert utils.to_millis(time_case.dt) == time_case.millis


def test_datetime_from_seconds(time_case):
    assert utils.datetime_from_seconds(time_case.seconds) == time_case.dt


def test_datetime_from_millis(time_case):
    assert utils.datetime_from_millis(time_case.millis) == time_case.dt


def test_datetime_from_str(time_case):
    assert utils.datetime_from_str(time_case.text) == time_case.dt


def test_datetime_from_str2():
    assert utils.datetime_from_str("2023-05-16T05:46:54.327313Z") == datetime.datetime(
        2023, 5, 16, 5, 46, 54, 327313, tzinfo=datetime.timezone.utc
    )


def test_inner():
    convert = utils.inner(lambda v: 2 * v, "x", "y")
    result = convert({"x": 42})
    assert result == {"x": 84}


def test_noop():
    assert "foo" == utils.noop("foo")


@pytest.fixture
def adapter_mapping():
    return {
        "foo_bar": "foo.bar",
        "baz": "baz",
        "qux": "foo.qux",
        "quux": "foo.quux",
        "corgeGrault": "foo.corge.grault",
        "corgeGarply": "foo.corge.garply",
    }


@pytest.fixture
def data_to_adapt():
    return {
        "foo": {
            "bar": "one",
            "qux": "three",
            "corge": {"grault": "four", "garply": None},
        },
        "baz": "two",
    }


def test_adapt_with_fill(adapter_mapping, data_to_adapt):
    adapt = utils.build_adapter(adapter_mapping)
    default = object()
    assert adapt(data_to_adapt, fill=True, default=default) == {
        "foo_bar": "one",
        "baz": "two",
        "qux": "three",
        "quux": default,
        "corgeGrault": "four",
        "corgeGarply": None,
    }


def test_adapt(adapter_mapping, data_to_adapt):
    adapt = utils.build_adapter(adapter_mapping)
    assert adapt(data_to_adapt) == {
        "foo_bar": "one",
        "baz": "two",
        "qux": "three",
        "corgeGrault": "four",
        "corgeGarply": None,
    }
