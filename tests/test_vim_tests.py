import subprocess
import tempfile
from io import BytesIO
from unittest import TestCase

from tests import stdout_redirected, stdin_redirected, project_root_dir
from xxd import HexDumper


def get_test_list():
    """Returns the test data list"""
    return "\n".join(str(s + 1) for s in range(30)) + "\n"


def get_xxd_of_test_list(start_line=0):
    """Returns the hex dump of the test data list"""
    data = (
            '00000000: 310a 320a 330a 340a 350a 360a 370a 380a  1.2.3.4.5.6.7.8.' + "\n"
            '00000010: 390a 3130 0a31 310a 3132 0a31 330a 3134  9.10.11.12.13.14' + "\n"
            '00000020: 0a31 350a 3136 0a31 370a 3138 0a31 390a  .15.16.17.18.19.' + "\n"
            '00000030: 3230 0a32 310a 3232 0a32 330a 3234 0a32  20.21.22.23.24.2' + "\n"
            '00000040: 350a 3236 0a32 370a 3238 0a32 390a 3330  5.26.27.28.29.30' + "\n"
            '00000050: 0a                                       .' + "\n"
    )
    line_length = len('00000000: 310a 320a 330a 340a 350a 360a 370a 380a  1.2.3.4.5.6.7.8.' + "\n")
    offset = line_length * start_line
    return data[offset:]


def prepare_buffer(lines):
    """Returns the binary version of the specified string"""
    output = lines.encode("utf-8")
    return output


class TestVimTests(TestCase):
    """Unit tests ported from
    https://github.com/vim/vim/blob/4ecf16bbf951f10fd32c918c9d8bc004b7f8f7c9/src/testdir/test_xxd.vim"""

    def test1(self):
        """Test_1: simple, filter the result through xxd"""
        indata = get_test_list()
        bindata = prepare_buffer(indata)
        with BytesIO(bindata) as infile:
            with stdin_redirected(infile):
                with BytesIO() as outfile:
                    with stdout_redirected(outfile):
                        args = {}
                        app = HexDumper(args)
                        app.run()
                        actual = outfile.getvalue()
        expected = prepare_buffer(get_xxd_of_test_list())
        self.assertEqual(expected, actual)

    def test2(self):
        """Test 2: reverse the result"""
        indata = get_xxd_of_test_list()
        bindata = prepare_buffer(indata)
        with BytesIO(bindata) as infile:
            with stdin_redirected(infile):
                with BytesIO() as outfile:
                    with stdout_redirected(outfile):
                        args = {
                            "reverse": True
                        }
                        app = HexDumper(args)
                        app.run()
                        actual = outfile.getvalue()
        expected = prepare_buffer(get_test_list())
        self.assertEqual(expected, actual)

    def test3(self):
        """Test 3: Skip the first 0x30 bytes"""

        # Create the input file, a list of numbers from 1 to 30
        _, testdata = tempfile.mkstemp()
        with open(testdata, "wt") as fp:
            fp.write(get_test_list())

        # Create the expected output file
        expected = get_xxd_of_test_list(start_line=3)
        _, expected_file = tempfile.mkstemp()
        with open(expected_file, "wt") as fp:
            fp.write(expected)

        # Now test a bunch of expressions for -s
        for arg in ['-s 0x30', '-s0x30', '-s+0x30', '-skip 0x030', '-seek 0x30', '-seek +0x30 --']:
            filename = "./pxxd"
            parms = [filename]
            for token in arg.split():
                parms.append(token)
            parms.append(testdata)
            _, outfile = tempfile.mkstemp()
            parms.append(outfile)

            # At this point, the "parms" list should consist of:
            #   The program to be called (pxxd)
            #   the args in arg, splitting on " " if necessary
            #   The input file name (testdata)
            #   The output file name (outfile)

            # Run the command
            cp = subprocess.run(parms, cwd=project_root_dir)
            if cp.returncode != 0:
                raise RuntimeError(f"Bad return code {cp.returncode} from running {parms[0]}")

            # Compare the results
            self.assertTrue(testdata, outfile)