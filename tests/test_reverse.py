import filecmp
import os
import subprocess
import tempfile
from unittest import TestCase, skip

from tests import project_root_dir, SaveDirectory, tmp, runxxd
from xxd import HexDumper


class TestReverse(TestCase):

    def test_reverse(self):
        # Create the temporary output file for xxd
        infile = os.path.join(tmp, "infile")
        indata = "Now is the time for all good men to come to the aid of their party.\n"
        with open(infile, "wt") as fp:
            fp.write(indata)

        # Run xxd on the file
        file1 = os.path.join(tmp, "file1")
        with SaveDirectory():
            os.chdir(project_root_dir)
            parms = ["xxd", infile, file1]
            runxxd(parms)

            # Now run pxxd to reverse the file transformation
            file2 = os.path.join(tmp, "file2")
            args = {
                "reverse": True,
                "infile": file1,
                "outfile": file2
            }
            app = HexDumper(args)
            app.run()

        # Are the files identical?
        self.assertTrue(filecmp.cmp(infile, file2))

        os.remove(infile)
        os.remove(file1)
        os.remove(file2)

    def test_reverse_with_seek(self):
        # Create the temporary output file for xxd
        infile = os.path.join(tmp, "infile")
        indata = "Now is the time for all good men to come to the aid of their party.\n"
        with open(infile, "wt") as fp:
            fp.write(indata)

        # Run xxd on the file
        with SaveDirectory():
            file1 = os.path.join(tmp, "file1")
            os.chdir(project_root_dir)
            parms = [
                "xxd",
                infile,
                file1
            ]
            runxxd(parms)

            # Now run pxxd to reverse the file transformation
            file2 = os.path.join(tmp, "file2")
            args = {
                "reverse": True,
                "seek": 4,
                "infile": file1,
                "outfile": file2
            }
            app = HexDumper(args)
            app.run()

        # Are the files identical?
        file1bytes = b'\x00\x00\x00\x00' + indata.encode("utf-8")
        with open(file2, "rb") as fp:
            file2bytes = fp.read()
        self.assertEqual(file1bytes, file2bytes)

        os.remove(infile)
        os.remove(file1)
        os.remove(file2)

    def test_reverse_ps(self):
        # Create the temporary output file for xxd
        infile = os.path.join(tmp, "infile")
        indata = "Now is the time for all good men to come to the aid of their party.\n"
        with open(infile, "wt") as fp:
            fp.write(indata)

        # Run xxd on the file
        with SaveDirectory():
            os.chdir(project_root_dir)
            file1 = os.path.join(tmp, "file1")
            parms = [
                "xxd",
                "-ps",
                infile,
                file1
            ]
            runxxd(parms)

            # Now run pxxd to reverse the file transformation
            file2 = os.path.join(tmp, "file2")
            args = {
                "reverse": True,
                "postscript": True,
                "infile": file1,
                "outfile": file2
            }
            app = HexDumper(args)
            app.run()

        # Are the files identical?
        self.assertTrue(filecmp.cmp(infile, file2))

        os.remove(infile)
        os.remove(file1)
        os.remove(file2)

    def test_reverse_ps_with_seek(self):
        # Create the temporary output file for xxd
        infile = os.path.join(tmp, "infile")
        indata = "Now is the time for all good men to come to the aid of their party.\n"
        with open(infile, "wt") as fp:
            fp.write(indata)

        # Run xxd on the file
        with SaveDirectory():
            os.chdir(project_root_dir)
            file1 = os.path.join(tmp, "file1")
            parms = [
                "xxd",
                "-ps",
                infile,
                file1
            ]
            runxxd(parms)

            # Now run pxxd to reverse the file transformation
            file2 = os.path.join(tmp, "file2")
            args = {
                "reverse": True,
                "postscript": True,
                "seek": 4,
                "infile": file1,
                "outfile": file2
            }
            app = HexDumper(args)
            app.run()

        # Are the files identical?
        file1bytes = b'\x00\x00\x00\x00' + indata.encode("utf-8")
        with open(file2, "rb") as fp:
            file2bytes = fp.read()
        self.assertEqual(file1bytes, file2bytes)

        os.remove(infile)
        os.remove(file1)
        os.remove(file2)
