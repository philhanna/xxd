from xxd import HexType


def test_for_circular_import():
    assert HexType.HEX_BITS.value == 3
