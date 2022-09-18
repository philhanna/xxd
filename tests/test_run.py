import filecmp
import os.path
import subprocess
import tempfile
from io import StringIO
from unittest import TestCase

from tests import project_root_dir, test_data_dir, stdout_redirected, stdin_redirected
from xxd import HexDumper


class TestRun(TestCase):

    def setUp(self) -> None:
        projectroot = project_root_dir
        testdata = test_data_dir

    def test_run_l_100(self):
        parms = ["xxd", "-l", "100", "testdata/cut"]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
        expected = str(cp.stdout, encoding="utf-8")

        args = {
            "len": 100,
            "infile": os.path.join(project_root_dir, "testdata/cut")
        }
        app = HexDumper(args)
        with StringIO() as out:
            with stdout_redirected(out):
                app.run()
            actual = out.getvalue()

        self.assertEqual(expected, actual)

    def test_run_o_x20(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-l", "100", "-o", "0x20", "testdata/cut", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "len": 100,
            "offset": "0x20",
            "infile": os.path.join(project_root_dir, "testdata/cut"),
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_run_hexadecimal(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "infile": os.path.join(project_root_dir, "testdata/short"),
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        #os.remove(file1)
        #os.remove(file2)

    def test_run_binary(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-b", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "binary": True,
            "infile": os.path.join(project_root_dir, "testdata/short"),
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        #os.remove(file1)
        #os.remove(file2)
