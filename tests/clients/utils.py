import pytest
import sys

from pydantic import TypeAdapter, ConfigDict, PydanticUserError


def skip_if_older_3_dot_10(fn):
    return pytest.mark.skipif(
        sys.version_info < (3, 10),
        reason="Too many incompatibilities with type hint",
    )(fn)


def validate(t: type, value: any):
    config = ConfigDict(strict=True, extra="forbid")

    class TWithConfig(t):
        __pydantic_config__ = config

    print("value", value)
    try:
        # In case `t` is a `TypedDict`
        return TypeAdapter(TWithConfig).validate_python(value)
    except PydanticUserError as exc_info:
        # In case `t` is a composition of `TypedDict`, like `list[TypedDict]`
        if exc_info.code == "schema-for-unknown-type":
            return TypeAdapter(t, config=config).validate_python(value)
        else:
            raise exc_info
