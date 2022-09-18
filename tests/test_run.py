import subprocess
from io import StringIO
from unittest import TestCase

from tests import stdout_redirected, project_root_dir, test_data_dir, stderr_redirected


class TestRun(TestCase):

    def setUp(self) -> None:
        testdata = test_data_dir

    def test_run_l_100(self):
        parms = ["xxd", "-l", "100", "testdata/cut"]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
        expected = str(cp.stdout, encoding="utf-8")

        parms[0] = "./pyxxd.py"
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
        actual = str(cp.stdout, encoding="utf-8")

        self.assertEqual(expected, actual)

    def test_run_o_x20(self):
        parms = ["xxd", "-l", "100", "-o", "0x20", "testdata/cut"]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
        expected = str(cp.stdout, encoding="utf-8")

        parms[0] = "./pyxxd.py"
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")
        actual = str(cp.stdout, encoding="utf-8")

        self.assertEqual(expected, actual)
