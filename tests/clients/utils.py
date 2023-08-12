from pydantic import TypeAdapter


def validate(t, value):
    # TODO: check exactly what `strict=True` enforce
    return TypeAdapter(t).validate_python(value, strict=True)
