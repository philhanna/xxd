import filecmp
import os
import subprocess
from io import StringIO
from unittest import TestCase

from tests import project_root_dir, stdout_redirected, stdin_redirected, SaveDirectory, tmp, runxxd, testdata
from xxd import HexDumper, PostscriptDumper


class TestHexDumperRun(TestCase):

    def test_postscript(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-ps", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "postscript": True,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = PostscriptDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test5(self):
        """Test 5: Print 120 bytes as continuous hexdump with 20 octets per line"""
        infile = os.path.join(testdata, "xxd.1")
        with StringIO() as fp, stdout_redirected(fp):
            args = {
                "postscript": True,
                "len": 120,
                "cols": 20,
                "infile": infile
            }
            app = PostscriptDumper(args)
            app.run()
            actual = fp.getvalue()

        filename = os.path.join(testdata, "man_copy.ps.expected")
        with open(filename, "rt") as fp:
            expected = fp.read()

        self.assertEqual(expected, actual)
