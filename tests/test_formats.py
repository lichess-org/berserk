from unittest import mock

from berserk import formats as fmts


def test_base_headers():
    fmt = fmts.FormatHandler("foo")
    assert fmt.headers == {"Accept": "foo"}


def test_base_handle():
    fmt = fmts.FormatHandler("foo")
    fmt.parse = mock.Mock(return_value="bar")
    fmt.parse_stream = mock.Mock()

    result = fmt.handle("baz", is_stream=False)
    assert result == "bar"
    assert fmt.parse_stream.call_count == 0


def test_base_handle_stream():
    fmt = fmts.FormatHandler("foo")
    fmt.parse = mock.Mock()
    fmt.parse_stream = mock.Mock(return_value="bar")

    result = fmt.handle("baz", is_stream=True)
    assert list(result) == list("bar")
    assert fmt.parse.call_count == 0


def test_json_handler_parse():
    fmt = fmts.JsonHandler("foo")
    m_response = mock.Mock()
    m_response.json.return_value = "bar"

    result = fmt.parse(m_response)
    assert result == "bar"


def test_json_handler_parse_stream():
    fmt = fmts.JsonHandler("foo")
    m_response = mock.Mock()
    m_response.iter_lines.return_value = [b'{"x": 5}', b"", b'{"y": 3}']

    result = fmt.parse_stream(m_response)
    assert list(result) == [{"x": 5}, {"y": 3}]


def test_pgn_handler_parse():
    fmt = fmts.PgnHandler()
    m_response = mock.Mock()
    m_response.text = "bar"

    result = fmt.parse(m_response)
    assert result == "bar"


def test_pgn_handler_parse_stream():
    fmt = fmts.PgnHandler()
    m_response = mock.Mock()
    m_response.iter_lines.return_value = [b"one", b"two", b"", b"", b"three"]

    result = fmt.parse_stream(m_response)
    assert list(result) == ["one\ntwo", "three"]
