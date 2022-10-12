from unittest import TestCase

from xxd import HexType, Dumper


class TestSetHexType(TestCase):

    def test_binary(self):
        args = {"binary": True}
        expected = HexType.HEX_BITS
        actual = Dumper.set_hextype(args)
        self.assertEqual(expected, actual)

    def test_little_endian(self):
        args = {"little_endian": True}
        expected = HexType.HEX_LITTLEENDIAN
        actual = Dumper.set_hextype(args)
        self.assertEqual(expected, actual)

    def test_c_include(self):
        args = {"include": True}
        expected = HexType.HEX_CINCLUDE
        actual = Dumper.set_hextype(args)
        self.assertEqual(expected, actual)

    def test_postscript(self):
        args = {"postscript": True}
        expected = HexType.HEX_POSTSCRIPT
        actual = Dumper.set_hextype(args)
        self.assertEqual(expected, actual)

    def test_normal(self):
        args = {}
        expected = HexType.HEX_NORMAL
        actual = Dumper.set_hextype(args)
        self.assertEqual(expected, actual)
