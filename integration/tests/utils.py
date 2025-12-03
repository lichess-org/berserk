import pytest
import pprint
import sys

from pydantic import TypeAdapter, ConfigDict, PydanticUserError


def validate(t: type, value: any):
    config = ConfigDict(strict=True, extra="forbid")

    class TWithConfig(t):
        __pydantic_config__ = config

    print("value")
    pprint.PrettyPrinter(indent=2).pprint(value)
    try:
        # In case `t` is a `TypedDict`
        adapter = TypeAdapter(TWithConfig)
        adapter.rebuild()
        return adapter.validate_python(value, strict=True, extra="forbid")
    except PydanticUserError as exc_info:
        raise exc_info
        # # In case `t` is a composition of `TypedDict`, like `list[TypedDict]`
        # if exc_info.code == "schema-for-unknown-type":
        #     return TypeAdapter(t, config=config).validate_python(value)
        # else:
        #     raise exc_info
