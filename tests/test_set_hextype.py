import pytest

from xxd import HexType, Dumper


@pytest.mark.parametrize("parms, expected", [
    ({}, HexType.HEX_NORMAL),
    ({"binary": True}, HexType.HEX_BITS),
    ({"little_endian": True}, HexType.HEX_LITTLEENDIAN),
    ({"include": True}, HexType.HEX_CINCLUDE),
    ({"postscript": True}, HexType.HEX_POSTSCRIPT),
])
def test_setting(parms, expected):
    assert Dumper.set_hextype(parms) == expected
