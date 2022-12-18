import pytest

from xxd import Dumper, HexType


@pytest.mark.parametrize("b,hextype,expected", [
    (0x23, HexType.HEX_BITS, "00100011"),
    (0x23, HexType.HEX_LITTLEENDIAN, "23"),
    (0x23, HexType.HEX_CINCLUDE, "23"),
    (0x23, HexType.HEX_POSTSCRIPT, "23"),
    (0x23, HexType.HEX_NORMAL, "23"),
])
def test_data_format(b, hextype, expected):
    assert Dumper.data_format(b, hextype) == expected
