# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from berserk import session
from berserk import utils


def test_request():
    m_session = mock.Mock()
    m_fmt = mock.Mock()
    requestor = session.Requestor(m_session, "http://foo.com/", m_fmt)

    result = requestor.request("bar", "path", baz="qux")

    assert result == m_fmt.handle.return_value

    args, kwargs = m_session.request.call_args
    assert ("bar", "http://foo.com/path") == args
    assert {"headers": m_fmt.headers, "baz": "qux"} == kwargs

    args, kwargs = m_fmt.handle.call_args
    assert (m_session.request.return_value,) == args
    assert {"is_stream": None, "converter": utils.noop} == kwargs


def test_bad_request():
    m_session = mock.Mock()
    m_session.request.return_value.ok = False
    m_session.request.return_value.raise_for_status.side_effect = Exception()
    m_fmt = mock.Mock()
    requestor = session.Requestor(m_session, "http://foo.com/", m_fmt)

    with pytest.raises(Exception):
        requestor.request("bar", "path", baz="qux")


def test_token_session():
    token_session = session.TokenSession("foo")
    assert token_session.token == "foo"
    assert token_session.headers == {"Authorization": "Bearer foo"}
