from unittest import TestCase

from xxd import HexType


class TestHexType(TestCase):
    def test_for_circular_import(self):
        print(f"DEBUG: {HexType.HEX_BITS=}")
