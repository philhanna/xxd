from unittest import TestCase

from xxd.pyxxd import parse_hex_digit


class TestParseHexDigit(TestCase):

    def test_digit_3(self):
        expected = 3
        actual = parse_hex_digit('3')
        self.assertEqual(expected, actual)

    def test_digit_0(self):
        expected = 0
        actual = parse_hex_digit('0')
        self.assertEqual(expected, actual)

    def test_digit_9(self):
        expected = 9
        actual = parse_hex_digit('9')
        self.assertEqual(expected, actual)

    def test_lc_hex_digit(self):
        expected = 11
        actual = parse_hex_digit('b')
        self.assertEqual(expected, actual)

    def test_uc_hex_digit(self):
        expected = 13
        actual = parse_hex_digit('D')
        self.assertEqual(expected, actual)

    def test_bogus(self):
        expected = -1
        actual = parse_hex_digit('%')
        self.assertEqual(expected, actual)

