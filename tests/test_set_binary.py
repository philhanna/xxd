from unittest import TestCase

from xxd import Dumper


class TestSetBinary(TestCase):

    def test_bogus(self):
        args = {"binary": "bogus"}
        with self.assertRaises(ValueError) as ve:
            Dumper.set_binary(args)
        errmsg = str(ve.exception)
        self.assertIn("is not True or False", errmsg)

    def test_default(self):
        args = {}
        expected = False
        actual = Dumper.set_binary(args)
        self.assertEqual(expected, actual)

    def test_false(self):
        args = {"binary": False}
        expected = False
        actual = Dumper.set_binary(args)
        self.assertEqual(expected, actual)

    def test_true(self):
        args = {"binary": True}
        expected = True
        actual = Dumper.set_binary(args)
        self.assertEqual(expected, actual)
