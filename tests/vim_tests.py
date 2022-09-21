import os
import struct
import tempfile
from io import StringIO, BytesIO
from unittest import TestCase

from tests import stdout_redirected
from xxd import HexDumper


def prepare_buffer(lines):
    output = lines.encode("utf-8")
    return output


class VimTests(TestCase):

    def test_1(self):
        """Test 1: simple, filter the result through xxd"""
        indata = "\n".join(str(s + 1) for s in range(30)) + "\n"
        bindata = prepare_buffer(indata)
        file1 = os.path.join(tempfile.gettempdir(), "test1.in.dat")
        with open(file1, "wb") as fp:
            for b in bindata:
                cb = struct.pack('B', b)
                fp.write(cb)
        expected = (
            '00000000: 310a 320a 330a 340a 350a 360a 370a 380a  1.2.3.4.5.6.7.8.' + "\n"
            '00000010: 390a 3130 0a31 310a 3132 0a31 330a 3134  9.10.11.12.13.14' + "\n"
            '00000020: 0a31 350a 3136 0a31 370a 3138 0a31 390a  .15.16.17.18.19.' + "\n"
            '00000030: 3230 0a32 310a 3232 0a32 330a 3234 0a32  20.21.22.23.24.2' + "\n"
            '00000040: 350a 3236 0a32 370a 3238 0a32 390a 3330  5.26.27.28.29.30' + "\n"
            '00000050: 0a                                       .' + "\n"
        )
        with StringIO() as file2:
            with stdout_redirected(file2):
                args = {
                    "infile": file1,
                }
                app = HexDumper(args)
                app.run()
                file2.flush()
                actual = file2.getvalue()

        self.assertEqual(expected, actual)