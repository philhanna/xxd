from unittest import TestCase

from xxd import HexType


class TestHexType(TestCase):
    def test_for_circular_import(self):
        expected = 3
        actual = HexType.HEX_BITS.value
        self.assertEqual(expected, actual)
