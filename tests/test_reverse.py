import os
import subprocess
import tempfile
from unittest import TestCase

from tests import project_root_dir
from xxd import HexDumper


class TestReverse(TestCase):

    def test_reverse(self):
        # Create the temporary output file for xxd
        _, infile = tempfile.mkstemp()
        indata = "Now is the time for all good men to come to the aid of their party."
        with open(infile, "wt") as fp:
            fp.write(indata + "\n")

        # Run xxd on the file
        _, file1 = tempfile.mkstemp()
        save_cwd = os.getcwd()
        try:
            os.chdir(project_root_dir)
            parms = [
                "xxd",
                infile,
                file1
            ]
            cp = subprocess.run(parms, stdout=subprocess.PIPE)
            if cp.returncode != 0:
                errmsg = f"Bad return code {cp.returncode} from running {parms[0]}"
                raise RuntimeError(errmsg)

            # Now run pxxd to reverse the file transformation
            _, file2 = tempfile.mkstemp()
            args = {
                "reverse": True,
                "infile": file1,
                "outfile": file2
            }
            app = HexDumper(args)
            app.run()
        finally:
            os.chdir(save_cwd)


