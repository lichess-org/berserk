from berserk import models


def test_conversion():
    class Example(models.Model):
        foo = int

    original = {"foo": "5", "bar": 3, "baz": "4"}
    modified = {"foo": 5, "bar": 3, "baz": "4"}
    assert Example.convert(original) == modified

def test_time_delta():
    """test timedelta_from millis"""
    test_data = 1000.0
    dt1 = datetime_from_millis(test_data)
    dt2 = datetime_from_millis(2 * test_data)

    delta_1 = timedelta_from_millis(test_data)

    # time delta dt1 dt2
    delta_2 = dt2 - dt1

    assert delta_1 == delta_2


