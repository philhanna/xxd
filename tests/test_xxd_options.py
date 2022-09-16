from unittest import TestCase

from xxd import XXD


class TestXXDOptions(TestCase):

    def test_binary_conflict_postscript(self):
        with self.assertRaises(ValueError) as err:
            XXD({"binary": True, "postscript": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_binary_conflict_include(self):
        with self.assertRaises(ValueError) as err:
            XXD({"binary": True, "include": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)

    def test_binary_conflict_reverse(self):
        with self.assertRaises(ValueError) as err:
            XXD({"binary": True, "reverse": True})
        errmsg = str(err.exception)
        self.assertIn("incompatible", errmsg)
