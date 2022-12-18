import filecmp
import subprocess
from pathlib import Path

import pytest

from tests import project_root_dir, stdout_redirected, stdin_redirected, SaveDirectory, tmp, runxxd
from xxd import HexDumper

CPGM = "xxd"
PPGM = "./pxxd"


def test_default(file1, file2):
    parms = [CPGM, "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_l_100():
    parms = [CPGM, "-l", "100", "testdata/cut"]
    cp = runxxd(parms)
    expected = cp.stdout

    parms = [PPGM, "-l", "100", "testdata/cut"]
    cp = runxxd(parms)
    actual = cp.stdout

    assert actual == expected


def test_o_x20(file1, file2):
    parms = [CPGM, "-l", "100", "-o", "0x20", "testdata/cut", file1]
    runxxd(parms)

    parms = [PPGM, "-l", "100", "-o", "0x20", "testdata/cut", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_binary(file1, file2):
    parms = [CPGM, "-b", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-b", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_columns_default(file1, file2):
    parms = [CPGM, "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_columns_10(file1, file2):
    parms = [CPGM, "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file1]
    runxxd(parms)

    parms = [CPGM, "-u", "-d", "-c", "10", "-o", "0x100", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_columns_20(file1, file2):
    parms = [CPGM, "-c", "20", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-c", "20", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_columns_too_great():
    args = {
        "cols": 2000,
        "infile": Path(project_root_dir).joinpath("testdata/short"),
    }
    with pytest.raises(ValueError) as x:
        HexDumper(args)
    errmsg = str(x.value)
    assert "columns" in errmsg


def test_ebcdic(file1, file2):
    parms = [CPGM, "-E", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-E", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_autoskip_allzero(file1, file2):
    parms = [CPGM, "-a", "testdata/allzero", file1]
    runxxd(parms)

    parms = [PPGM, "-a", "testdata/allzero", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_autoskip_mixed(file1, file2):
    parms = [CPGM, "-a", "testdata/mixedzero", file1]
    runxxd(parms)

    parms = [PPGM, "-a", "testdata/mixedzero", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_seek(file1, file2):
    parms = [CPGM, "-s", "0x20", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-s", "0x20", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_seek_past_end(file1, file2):
    parms = [CPGM, "-s", "0x100", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-s", "0x100", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_seek_with_stdin(file1, file2):
    """ Unit test with --seek and stdin"""
    parms = [CPGM, "-s", "0x01", "-", file1]
    subprocess.run(parms,
                   cwd=project_root_dir,
                   check=True,
                   text=True,
                   input="abcdefg",
                   capture_output=True)

    parms = [PPGM, "-s", "0x01", "-", file2]
    subprocess.run(parms,
                   cwd=project_root_dir,
                   check=True,
                   text=True,
                   input="abcdefg",
                   capture_output=True)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_dont_show_traceback():
    parms = [PPGM, "bogus"]
    cp = runxxd(parms)
    errmsg = cp.stdout
    assert "No such file or directory" in errmsg
