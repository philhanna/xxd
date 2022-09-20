import filecmp
import os
import subprocess
import tempfile
from io import StringIO
from unittest import TestCase

from tests import project_root_dir, test_data_dir, stdout_redirected, stdin_redirected
from xxd import HexDumper


class TestRun(TestCase):

    def test_default(self):
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
        os.remove(file1)
        os.remove(file2)

    def test_l_100(self):
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

    def test_o_x20(self):
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

    def test_binary(self):
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
        os.remove(file1)
        os.remove(file2)

    def test_columns_default(self):
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
        os.remove(file1)
        os.remove(file2)

    def test_columns_10(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "cols": 10,
            "decimal": True,
            "uppercase": True,
            "offset": "0x100",
            "infile": os.path.join(project_root_dir, "testdata/short"),
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_columns_20(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-c", "20", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "cols": 20,
            "infile": os.path.join(project_root_dir, "testdata/short"),
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_include(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-i", "-l", "60", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "include": True,
            "len": 60,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_ebcdic(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-E", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "EBCDIC": True,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_postscript(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-ps", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "postscript": True,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_name(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-i", "-n", "3om", "testdata/short", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "include": True,
            "name": "3om",
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_allzero(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-a", "testdata/allzero", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "autoskip": True,
            "infile": "testdata/allzero",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_mixed(self):
        file1 = os.path.join(tempfile.gettempdir(), "file1")
        parms = ["xxd", "-a", "testdata/mixedzero", file1]
        cp = subprocess.run(parms, cwd=project_root_dir, stdout=subprocess.PIPE)
        if cp.returncode != 0:
            raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

        file2 = os.path.join(tempfile.gettempdir(), "file2")
        args = {
            "autoskip": True,
            "infile": "testdata/mixedzero",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        save_cwd = os.getcwd()
        os.chdir(project_root_dir)
        app = HexDumper(args)
        app.run()
        os.chdir(save_cwd)

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)
