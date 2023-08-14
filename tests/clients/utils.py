from pydantic import TypeAdapter, ConfigDict


def validate(t, value):
    # TODO: check exactly what `strict=True` enforce
    class TWithConfig(t):
        __pydantic_config__ = ConfigDict(strict=True, extra="forbid")

    return TypeAdapter(TWithConfig).validate_python(value)
