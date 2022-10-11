import filecmp
import os
import subprocess
import tempfile
from io import StringIO
from unittest import TestCase

from tests import project_root_dir, stdout_redirected, stdin_redirected, SaveDirectory
from xxd import HexDumper

tmp = tempfile.gettempdir()


def runxxd(parms) -> subprocess.CompletedProcess:
    return subprocess.run(parms,
                          cwd=project_root_dir,
                          check=True,
                          text=True,
                          capture_output=True)


class TestHexDumperRun(TestCase):

    def test_default(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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
        cp = runxxd(parms)
        expected = cp.stdout

        args = {
            "len": 100,
            "infile": os.path.join(project_root_dir, "testdata/cut")
        }
        app = HexDumper(args)
        with StringIO() as out, stdout_redirected(out):
            app.run()
            actual = out.getvalue()

        self.assertEqual(expected, actual)

    def test_o_x20(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-l", "100", "-o", "0x20", "testdata/cut", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-b", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-c", "20", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
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

    def test_columns_too_great(self):
        args = {
            "cols": 2000,
            "infile": os.path.join(project_root_dir, "testdata/short"),
        }
        with self.assertRaises(ValueError) as x:
            HexDumper(args)
        errmsg = str(x.exception)
        self.assertIn("columns", errmsg)

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
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_ebcdic(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-E", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "EBCDIC": True,
            "infile": "testdata/short",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

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
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_name(self):
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
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_allzero(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-a", "testdata/allzero", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "autoskip": True,
            "infile": "testdata/allzero",
            "outfile": file2
        }

        # Need to chdir so that the input file is found.
        # I can't specify a full path because that's what is used
        # to form the varname of the include file
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_autoskip_mixed(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-a", "testdata/mixedzero", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "autoskip": True,
            "infile": "testdata/mixedzero",
            "outfile": file2
        }

        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-s", "0x20", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "seek": 0x20,
            "infile": "testdata/short",
            "outfile": file2
        }

        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek_past_end(self):
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-s", "0x100", "testdata/short", file1]
        runxxd(parms)

        file2 = os.path.join(tmp, "file2")
        args = {
            "seek": "0x100",
            "infile": "testdata/short",
            "outfile": file2
        }
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_seek_with_stdin(self):
        """ Unit test with --seek and stdin"""
        file1 = os.path.join(tmp, "file1")
        parms = ["xxd", "-s", "0x01", "-", file1]
        subprocess.run(parms,
                       cwd=project_root_dir,
                       check=True,
                       text=True,
                       input="abcdefg",
                       capture_output=True)

        with (StringIO("abcdefg") as fpin,
              stdin_redirected(fpin),
              SaveDirectory()):
            file2 = os.path.join(tmp, "file2")
            args = {
                "seek": "0x01",
                "outfile": file2
            }
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_dont_show_traceback(self):
        parms = ["./pxxd", "bogus"]
        cp = runxxd(parms)
        errmsg = cp.stdout
        self.assertIn("No such file or directory", errmsg)

    def test_ps_reverse(self):
        input_string = "4b52414d4552202d2052454d41524b0a"
        input_pairs = [input_string[i:i + 2]
                       for i in range(0, len(input_string), 2)]
        input_chars = [chr(int(x, 16)) for x in input_pairs]
        s = "".join(input_chars)
        file1 = os.path.join(tmp, "file1")
        with open(file1, "wb") as fp:
            fp.write(s.encode("utf-8"))

        file2 = os.path.join(tmp, "file2")
        args = {
            "reverse": True,
            "postscript": True,
            "infile": "testdata/shortline",
            "outfile": file2,
        }
        with SaveDirectory():
            os.chdir(project_root_dir)
            app = HexDumper(args)
            app.run()

        self.assertTrue(filecmp.cmp(file1, file2))
        os.remove(file1)
        os.remove(file2)

    def test_ps_reverse_stdout(self):
        input_string = "4b52414d4552202d2052454d41524b"
        input_pairs = [input_string[i:i + 2]
                       for i in range(0, len(input_string), 2)]
        input_chars = [chr(int(x, 16)) for x in input_pairs]
        expected = "".join(input_chars)
        with (StringIO(input_string) as fpin,
              stdin_redirected(fpin),
              StringIO() as fpout,
              stdout_redirected(fpout)):
            args = {
                "reverse": True,
                "postscript": True,
            }
            app = HexDumper(args)
            app.run()
            actual = fpout.getvalue()
        self.assertEqual(expected, actual)
