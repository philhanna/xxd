from unittest import TestCase

from xxd import Dumper, HexType


class TestDataFormat(TestCase):

    def test_data_format_binary(self):
        b = 0x23
        expected = "00100011"
        actual = Dumper.data_format(b, HexType.HEX_BITS)
        self.assertEqual(expected, actual)

    def test_data_format_little_endian(self):
        b = 0x23
        expected = "23"
        actual = Dumper.data_format(b, HexType.HEX_LITTLEENDIAN)
        self.assertEqual(expected, actual)

    def test_data_format_c_include(self):
        b = 0x23
        expected = "23"
        actual = Dumper.data_format(b, HexType.HEX_CINCLUDE)
        self.assertEqual(expected, actual)

    def test_data_format_postscript(self):
        b = 0x23
        expected = "23"
        actual = Dumper.data_format(b, HexType.HEX_POSTSCRIPT)
        self.assertEqual(expected, actual)

    def test_data_format_normal(self):
        b = 0x23
        expected = "23"
        actual = Dumper.data_format(b, HexType.HEX_NORMAL)
        self.assertEqual(expected, actual)
