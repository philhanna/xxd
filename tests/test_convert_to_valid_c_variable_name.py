from unittest import TestCase

from xxd import HexDumper, CDumper


class TestConvertToValidCVariableName(TestCase):

    def test_0(self):
        name = "foo"
        expected = "foo"
        actual = CDumper.convert_to_valid_c_variable_name(name)
        self.assertEqual(expected, actual)

    def test_1(self):
        bad_name = "3"
        expected = "__3"
        actual = CDumper.convert_to_valid_c_variable_name(bad_name)
        self.assertEqual(expected, actual)

    def test_2(self):
        bad_name = "testdata/short"
        expected = "testdata_short"
        actual = CDumper.convert_to_valid_c_variable_name(bad_name)
        self.assertEqual(expected, actual)

    def test_3(self):
        bad_name = "3testdata/short"
        expected = "__3testdata_short"
        actual = CDumper.convert_to_valid_c_variable_name(bad_name)
        self.assertEqual(expected, actual)

    def test_4(self):
        bad_name = " "
        expected = "_"
        actual = CDumper.convert_to_valid_c_variable_name(bad_name)
        self.assertEqual(expected, actual)
