import filecmp
from io import StringIO
from os import chdir
from pathlib import Path

from tests import project_root_dir, stdout_redirected, stdin_redirected, SaveDirectory, tmp, runxxd, testdata
from xxd import PostscriptDumper

CPGM = "xxd"
PPGM = "./pxxd"


def test_postscript(file1, file2):
    parms = [CPGM, "-ps", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-ps", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test5():
    """Test 5: Print 120 bytes as continuous hexdump with 20 octets per line"""
    infile = Path(testdata).joinpath("xxd.1")
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

    filename = Path(testdata).joinpath("man_copy.ps.expected")
    with open(filename, "rt") as fp:
        expected = fp.read()

    assert actual == expected


def test_ps_reverse(file1, file2):
    input_string = "4b52414d4552202d2052454d41524b0a"
    input_pairs = [input_string[i:i + 2]
                   for i in range(0, len(input_string), 2)]
    input_chars = [chr(int(x, 16)) for x in input_pairs]
    s = "".join(input_chars)
    with open(file1, "wb") as fp:
        fp.write(s.encode("utf-8"))

    args = {
        "reverse": True,
        "postscript": True,
        "infile": "testdata/shortline",
        "outfile": file2,
    }
    with SaveDirectory():
        chdir(project_root_dir)
        app = PostscriptDumper(args)
        app.run()

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_ps_reverse_stdout():
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
        app = PostscriptDumper(args)
        app.run()
        actual = fpout.getvalue()
    assert actual == expected
