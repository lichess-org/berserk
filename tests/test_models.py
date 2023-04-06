from berserk import models


def test_conversion():
    class Example(models.Model):
        foo = int

    original = {"foo": "5", "bar": 3, "baz": "4"}
    modified = {"foo": 5, "bar": 3, "baz": "4"}
    assert Example.convert(original) == modified
