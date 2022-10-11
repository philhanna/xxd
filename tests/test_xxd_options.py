from unittest import TestCase

from xxd import HexDumper, CDumper, PostscriptDumper


class TestXXDOptions(TestCase):

    def test_autoskip_default(self):
        xxd = HexDumper({})
        self.assertFalse(xxd.autoskip)

    def test_autoskip_true(self):
        xxd = HexDumper({"autoskip": True})
        self.assertTrue(xxd.autoskip)

    def test_binary_conflict_include(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"binary": True, "include": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    # The -b option is incompatible with -ps, -i, or -r
    def test_binary_conflict_postscript(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"binary": True, "postscript": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_binary_conflict_reverse(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"binary": True, "reverse": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_cols_binary(self):
        xxd = HexDumper({"binary": True})
        expected = 6
        actual = xxd.cols
        self.assertEqual(expected, actual)

    # Cols has different defaults depending on whether -ps or -i have been specified
    def test_cols_default(self):
        xxd = HexDumper({})
        expected = 16
        actual = xxd.cols
        self.assertEqual(expected, actual)

    def test_cols_postscript(self):
        xxd = PostscriptDumper({"postscript": True})
        expected = 30
        actual = xxd.cols
        self.assertEqual(expected, actual)

    def test_cols_include(self):
        xxd = CDumper({"include": True})
        expected = 12
        actual = xxd.cols
        self.assertEqual(expected, actual)

    def test_decimal(self):
        xxd = HexDumper({"decimal": True})
        self.assertTrue(xxd.decimal)

    def test_e_conflict_include(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"little_endian": True, "include": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    # The -e option is incompatible with -ps, -i, or -r
    def test_e_conflict_postscript(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"little_endian": True, "postscript": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_e_conflict_reverse(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"little_endian": True, "reverse": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_EBCDIC(self):
        xxd = HexDumper({})
        self.assertFalse(xxd.EBCDIC)

    def test_g_b(self):
        xxd = HexDumper({"binary": True})
        expected = 1
        actual = xxd.octets_per_group
        self.assertEqual(expected, actual)

    # Octets_per_group has different defaults depending on whether -e has been specified
    def test_g_default(self):
        xxd = HexDumper({})
        expected = 2
        actual = xxd.octets_per_group
        self.assertEqual(expected, actual)

    def test_g_e(self):
        xxd = HexDumper({"little_endian": True})
        expected = 4
        actual = xxd.octets_per_group
        self.assertEqual(expected, actual)

    def test_g_ps(self):
        xxd = HexDumper({"postscript": True})
        expected = 2
        actual = xxd.octets_per_group
        self.assertEqual(expected, actual)

    def test_include_default(self):
        xxd = HexDumper({})
        self.assertFalse(xxd.include)

    def test_infile(self):
        xxd = HexDumper({"infile": "/usr/bin/cut"})
        expected = "/usr/bin/cut"
        actual = xxd.infile
        self.assertEqual(expected, actual)

    def test_infile_default(self):
        xxd = HexDumper({})
        self.assertIsNone(xxd.infile)

    def test_infile_stdin(self):
        xxd = HexDumper({"infile": "-"})
        expected = "-"
        actual = xxd.infile
        self.assertEqual(expected, actual)

    def test_len(self):
        xxd = HexDumper({"len": "13"})
        expected = 13
        actual = xxd.length
        self.assertEqual(expected, actual)

    def test_len_bogus(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"len": "bogus"})
        errmsg = str(err.exception)
        self.assertIn("not numeric", errmsg)

    def test_len_default(self):
        xxd = HexDumper({})
        self.assertIsNone(xxd.length)

    def test_len_negative(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"len": "-1"})
        errmsg = str(err.exception)
        self.assertIn("negative", errmsg)

    def test_len_zero(self):
        xxd = HexDumper({"len": "0"})
        expected = 0
        actual = xxd.length
        self.assertEqual(expected, actual)

    def test_name(self):
        xxd = HexDumper({"name": "wonderful"})
        expected = "wonderful"
        actual = xxd.name
        self.assertEqual(expected, actual)

    def test_name_default(self):
        xxd = HexDumper({})
        expected = None
        actual = xxd.name
        self.assertEqual(expected, actual)

    def test_offset(self):
        xxd = HexDumper({"offset": 0x100})
        expected = 256
        actual = xxd.offset
        self.assertEqual(expected, actual)

    def test_offset_bogus(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"offset": "bogus"})
        errmsg = str(err.exception)
        self.assertIn("numeric", errmsg)

    def test_offset_default(self):
        xxd = HexDumper({})
        expected = 0
        actual = xxd.offset
        self.assertEqual(expected, actual)

    def test_offset_negative(self):
        with self.assertRaises(ValueError) as err:
            HexDumper({"offset": -86})
        errmsg = str(err.exception)
        self.assertIn("negative", errmsg)

    def test_outfile(self):
        xxd = HexDumper({})
        self.assertIsNone(xxd.outfile)

    def test_pname(self):
        xxd = HexDumper({})
        self.assertIsNotNone(xxd.pname)

    def test_postscript(self):
        xxd = HexDumper({"postscript": True})
        self.assertTrue(xxd.postscript)

    def test_reverse(self):
        xxd = HexDumper({"reverse": True})
        self.assertTrue(xxd.reverse)

    def test_seek(self):
        xxd = HexDumper({"seek": 0x0100})
        expected = 256
        actual = xxd.seek
        self.assertEqual(expected, actual)

    def test_seek_default(self):
        xxd = HexDumper({})
        expected = None
        actual = xxd.seek
        self.assertEqual(expected, actual)

    def test_uppercase(self):
        xxd = HexDumper({"uppercase": True})
        self.assertTrue(xxd.uppercase)

    def test_version(self):
        xxd = HexDumper({"version": True})
        self.assertTrue(xxd.version)

