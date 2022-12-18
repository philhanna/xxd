import pytest

from xxd import CDumper


@pytest.mark.parametrize("name,expected", [
    ("foo", "foo"),
    ("3", "__3"),
    ("testdata/short", "testdata_short"),
    ("3testdata/short", "__3testdata_short"),
    (" ", "_"),
])
def test_conversion(name, expected):
    assert CDumper.convert_to_valid_c_variable_name(name) == expected
