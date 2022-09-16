from unittest import TestCase

from xxd import HexDumper


class TestRun(TestCase):

    def test_run_with_version(self):
        with self.assertRaises(SystemExit) as err:
            xxd = HexDumper({"version": True})
            xxd.run()
        errmsg = str(err.exception)
        self.assertEqual("0", errmsg)
