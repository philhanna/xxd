import filecmp
import os
from io import StringIO
from unittest import TestCase

from tests import tmp, runxxd, SaveDirectory, project_root_dir, stdout_redirected
from xxd import CDumper


class TestCDumperRun(TestCase):

    def test_include(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-i", "-l", "60", "-C", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "include": True,
            "len": 60,
            "capitalize": True,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = CDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_varname(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-i", "-n", "3om", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "include": True,
            "name": "3om",
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = CDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_vim_7(self):
        """Test 7: Print C include"""
        indata = "TESTabcd09\n"
        file1 = os.path.join(tmp, "XXDFile")
        with open(file1, "wt") as fp:
            fp.write(indata)

        with StringIO() as out, stdout_redirected(out):
            args = {
                "include": True,
                "infile": file1,
                "name": "XXDFile",
            }
            app = CDumper(args)
            app.run()
            actual = out.getvalue()

        expected = """\
unsigned char XXDFile[] = {
  0x54, 0x45, 0x53, 0x54, 0x61, 0x62, 0x63, 0x64, 0x30, 0x39, 0x0a
};
unsigned int XXDFile_len = 11;
"""
        self.assertEqual(expected, actual)
        os.remove(file1)

    def test_vim_8(self):
        """Test 8: Print C include capitalized"""
        indata = "TESTabcd09\n"
        file1 = os.path.join(tmp, "XXDFile")
        with open(file1, "wt") as fp:
            fp.write(indata)

        with StringIO() as out, stdout_redirected(out):
            args = {
                "include": True,
                "infile": file1,
                "capitalize": True,
                "name": "XXDFile",
            }
            app = CDumper(args)
            app.run()
            actual = out.getvalue()

        expected = """\
unsigned char XXDFILE[] = {
  0x54, 0x45, 0x53, 0x54, 0x61, 0x62, 0x63, 0x64, 0x30, 0x39, 0x0a
};
unsigned int XXDFILE_LEN = 11;
"""
        self.assertEqual(expected, actual)
