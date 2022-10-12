import filecmp
import os
import subprocess
from io import StringIO
from unittest import TestCase

from tests import project_root_dir, stdout_redirected, stdin_redirected, SaveDirectory, tmp, runxxd
from xxd import HexDumper

CPGM = "xxd"
PPGM = "./pxxd"


class TestDumperRunHex(TestCase):

    def test_default(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_l_100(self):
        parms = [CPGM, "-l", "100", "testdata/cut"]
        cp = runxxd(parms)
        expected = cp.stdout

        parms = [PPGM, "-l", "100", "testdata/cut"]
        cp = runxxd(parms)
        actual = cp.stdout

        self.assertEqual(expected, actual)

    def test_o_x20(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-l", "100", "-o", "0x20", "testdata/cut", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-l", "100", "-o", "0x20", "testdata/cut", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_binary(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-b", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-b", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_columns_default(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_columns_10(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [CPGM, "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_columns_20(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-c", "20", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-c", "20", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_columns_too_great(self):
        args = {
            "cols": 2000,
            "infile": os.path.join(project_root_dir, "testdata/short"),
        }
        with self.assertRaises(ValueError) as x:
            HexDumper(args)
        errmsg = str(x.exception)
        self.assertIn("columns", errmsg)

    def test_ebcdic(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-E", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-E", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_allzero(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-a", "testdata/allzero", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-a", "testdata/allzero", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_mixed(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-a", "testdata/mixedzero", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-a", "testdata/mixedzero", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-s", "0x20", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-s", "0x20", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek_past_end(self):
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-s", "0x100", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-s", "0x100", "testdata/short", file2]
        runxxd(parms)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek_with_stdin(self):
        """ Unit test with --seek and stdin"""
        file1 = os.path.join(tmp, "file1")
        parms = [CPGM, "-s", "0x01", "-", file1]
        subprocess.run(parms,
                       cwd=project_root_dir,
                       check=True,
                       text=True,
                       input="abcdefg",
                       capture_output=True)

        file2 = os.path.join(tmp, "file2")
        parms = [PPGM, "-s", "0x01", "-", file2]
        subprocess.run(parms,
                       cwd=project_root_dir,
                       check=True,
                       text=True,
                       input="abcdefg",
                       capture_output=True)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_dont_show_traceback(self):
        parms = [PPGM, "bogus"]
        cp = runxxd(parms)
        errmsg = cp.stdout
        self.assertIn("No such file or directory", errmsg)
