from unittest import TestCase

from xxd import HexDumper


class TestRun(TestCase):

    def test_run_with_version(self):
        xxd = HexDumper()
