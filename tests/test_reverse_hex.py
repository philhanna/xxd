import filecmp
from os import chdir
from pathlib import Path

from tests import project_root_dir, SaveDirectory, tmp, runxxd
from xxd import HexDumper


def test_reverse(file1, file2):
    # Create the temporary output file for xxd
    infile = Path(tmp).joinpath("infile")
    indata = "Now is the time for all good men to come to the aid of their party.\n"
    with open(infile, "wt") as fp:
        fp.write(indata)

    # Run xxd on the file
    with SaveDirectory():
        chdir(project_root_dir)
        parms = ["xxd", infile, file1]
        runxxd(parms)

        # Now run pxxd to reverse the file transformation
        args = {
            "reverse": True,
            "infile": file1,
            "outfile": file2
        }
        app = HexDumper(args)
        app.run()

    # Are the files identical?
    assert filecmp.cmp(infile, file2)

    infile.unlink()
    file1.unlink()
    file2.unlink()


def test_reverse_with_seek(file1, file2):
    # Create the temporary output file for xxd
    infile = Path(tmp).joinpath("infile")
    indata = "Now is the time for all good men to come to the aid of their party.\n"
    with open(infile, "wt") as fp:
        fp.write(indata)

    # Run xxd on the file
    with SaveDirectory():
        chdir(project_root_dir)
        parms = [
            "xxd",
            infile,
            file1
        ]
        runxxd(parms)

        # Now run pxxd to reverse the file transformation
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
    assert file1bytes == file2bytes

    infile.unlink()
    file1.unlink()
    file2.unlink()
