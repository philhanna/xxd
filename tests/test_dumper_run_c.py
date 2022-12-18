import filecmp
from io import StringIO
from pathlib import Path

from tests import tmp, runxxd, stdout_redirected
from xxd import CDumper

CPGM = "xxd"
PPGM = "./pxxd"


def test_include(file1, file2):
    parms = [CPGM, "-i", "-l", "60", "-C", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-i", "-l", "60", "-C", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_varname(file1, file2):
    parms = [CPGM, "-i", "-n", "3om", "testdata/short", file1]
    runxxd(parms)

    parms = [PPGM, "-i", "-n", "3om", "testdata/short", file2]
    runxxd(parms)

    assert filecmp.cmp(file1, file2)
    file1.unlink()
    file2.unlink()


def test_vim_7():
    """Test 7: Print C include"""
    indata = "TESTabcd09\n"
    file1 = Path(tmp).joinpath("XXDFile")
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
    assert actual == expected
    file1.unlink()


def test_vim_8():
    """Test 8: Print C include capitalized"""
    indata = "TESTabcd09\n"
    file1 = Path(tmp).joinpath("XXDFile")
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
    assert actual == expected
    file1.unlink()
