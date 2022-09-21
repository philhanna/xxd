import subprocess
import sys
import tempfile
from io import StringIO, BytesIO
from unittest import TestCase

from tests import project_root_dir, stdin_redirected


class TestReverse(TestCase):

    def test_reverse(self):
        # Create the temporary output file for xxd
        _, a = tempfile.mkstemp()
        indata = "Now is the time for all good men to come to the aid of their party."
        with StringIO(indata) as fp:
            with stdin_redirected(fp):
                parms = ["xxd"]
                cp = subprocess.run(parms,
                                    input=sys.stdin,
                                    cwd=project_root_dir,
                                    stdout=subprocess.PIPE)
                if cp.returncode != 0:
                    errmsg = f"Bad return code {cp.returncode} from running {parms[0]}"
                    raise RuntimeError(errmsg)

        # Create temporary file for the output of xxd -r
        _, b = tempfile.mkstemp()
        parms = ["xxd", "-r", a, b]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
