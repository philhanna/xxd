from unittest import TestCase
import os.path
from tests import test_data_dir
from xxd import HexDumper


class TestMainline(TestCase):

    def setUp(self):
        self.input_file = os.path.join(test_data_dir, "cut")
        self.args = {"infile": self.input_file}
        self.xxd = HexDumper(self.args)

    def tearDown(self) -> None:
        del self.args
        del self.xxd
