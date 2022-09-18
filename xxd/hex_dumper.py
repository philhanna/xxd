import os.path
import sys
from io import UnsupportedOperation

from xxd import HexType, COLS


class HexDumper:
    """Python version of Juergen Weigert's xxd"""

    def mainline(self):
        """Runs the hex dumper"""

        # Debugging for issue #12:

        print(f"DEBUG: Arguments at beginning of mainline:")
        for k, v in self.args.items():
            print(f"DEBUG: {k:20s} = {v}")

        offset = 0
        so_far = 0
        if hasattr(self, "seek"):
            if self.seek is not None:
                seek = self.seek
                if type(seek) != int:
                    seek = int(seek, 0)
                try:
                    self.fpin.seek(seek)
                except UnsupportedOperation as e:
                    for i in range(seek):
                        self.fpin.read(1)
                offset += seek

        while True:
            # Add entries to the chunk_size table as needed
            chunk_size: int = {
                HexType.HEX_BITS: 6,
                HexType.HEX_NORMAL: 16,
            }.get(self.hextype, 16)

            if hasattr(self, "length"):
                if so_far + chunk_size > self.length:
                    chunk_size = self.length % chunk_size
            data = self.fpin.read(chunk_size)
            if len(data) == 0:
                break
            if type(data) == str:
                data = bytes(data.encode("utf-8"))

            data_list = []
            data_length = len(data)
            for i in range(0, data_length, self.octets_per_group):
                chunk_slice = slice(i, i + self.octets_per_group, 1)
                chunk_bytes = data[chunk_slice]
                data_list.append(chunk_bytes)

            hex_list = []
            text_list = []

            for chunk_bytes in data_list:
                sb = ""
                for chunk_byte in chunk_bytes:
                    sb += self.data_format(chunk_byte)
                hex_list.append(sb)

                sb = ""
                for chunk_byte in chunk_bytes:
                    sb += self.text_format(chunk_byte)
                text_list.append(sb)

            sdata = " ".join(hex_list)
            # print(f"DEBUG: sdata={sdata}")
            if self.uppercase:
                sdata = sdata.upper()
            text = "".join(text_list)
            offset_shown = offset
            if hasattr(self, "offset"):
                if self.offset is not None:
                    if type(self.offset) != int:
                        self.offset = int(self.offset, 0)
                    add_offset = self.offset
                    offset_shown += add_offset
            if self.decimal:
                offset_format_str = "08d"
            else:
                offset_format_str = "08x"

            chars_per_hextype: int = {
                HexType.HEX_BITS: 8,
                HexType.HEX_NORMAL: 2,
            }.get(self.hextype, 2)

            n_groups = int(self.cols / self.octets_per_group)
            group_width = 1 + self.octets_per_group * chars_per_hextype
            data_width = n_groups * group_width
            line = f"{offset_shown:{offset_format_str}}: {sdata:{data_width}s} {text}\n"
            bline = line.encode('utf-8')
            #print(f"DEBUG: {bline=}")
            try:
                self.fpout.write(bline)
            except TypeError as e:
                self.fpout.write(line)
            self.fpout.flush()
            offset += chunk_size
            so_far += len(data)
            if hasattr(self, "length"):
                length = self.length
                if so_far >= length:
                    break

    def data_format(self, b):
        result = None
        if self.hextype == HexType.HEX_BITS:
            result = format(b, "08b")
        else:
            result = format(b, "02x")
        return result

    @staticmethod
    def text_format(c: int):
        if c < 128 and chr(c).isprintable():
            return chr(c)
        else:
            return "."

    def run(self):
        """Calls mainline with specified input and output files"""

        # Check for infile.  If not specified, or if it is "-", use stdin.
        # Otherwise, try to open the file.
        # If outfile is specified, open it for writing, otherwise, use stdout.

        self.fpin = None
        self.fpout = None
        try:
            if self.infile is None or self.infile == sys.stdin or self.infile == '-':
                self.fpin = sys.stdin
            else:
                self.fpin = open(self.infile, "rb")

            if self.outfile is None or self.outfile == sys.stdout:
                self.fpout = sys.stdout
            else:
                self.fpout = open(self.outfile, "wb")

            # Run the mainline
            self.mainline()

        # Close the files
        finally:
            if self.fpin is not None:
                if self.fpin != sys.stdin:
                    self.fpin.close()
            if self.fpout is not None:
                self.fpout.flush()
                if self.fpout != sys.stdout:
                    self.fpout.close()

    def __init__(self, args: dict = {}):
        """Creates a new XXD object with specified options.
        Note that defaults are implemented here by the dictionary 'get(key, default)' approach.
        Incompatible options raise a ValueError.
        """

        self.args = args

        self.pname: str = sys.argv[0].split("/")[-1]
        self.fpin = None
        self.fpout = None
        self.autoskip: bool = args.get("autoskip", False)
        self.hextype = HexType.HEX_NORMAL

        # Binary option is incompatible with -ps, -i, or -r
        self.binary: bool = args.get("binary", False)
        if self.binary:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys() and args[other]:
                    raise ValueError("-b option is incompatible with -ps, -i, or -r.")
            self.hextype = HexType.HEX_BITS

        self.capitalize: bool = args.get("capitalize", False)

        # Cols option has different defaults depending on whether -ps or -i have been specified
        if args.get("postscript", False):
            self.cols = 30
        elif args.get("include", False):
            self.cols = 12
        elif self.binary:
            self.cols = 6
        else:
            self.cols = 16
        if "cols" in args:  # See if an override was specified
            attr_cols = args.get("cols", None)
            if attr_cols is not None:
                try:
                    if type(attr_cols) != int:
                        attr_cols: int = int(attr_cols, 0)
                    self.cols = attr_cols
                except ValueError as e:
                    errmsg = f"-c {attr_cols} is not numeric"
                    raise ValueError(errmsg)
                if self.cols < 0:
                    raise ValueError(f"-c {attr_cols} is not a non-negative integer")

        if self.cols > COLS:
            raise ValueError("Number of columns {self.cols} cannot be greater than {COLS}")

        self.EBCDIC: bool = args.get("EBCDIC", False)

        # Little endian option is incompatible with -ps, -i, or -r
        self.little_endian: bool = args.get("little_endian", False)
        if self.little_endian:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-e option is incompatible with -ps, -i, or -r.")

        # Octets per group option has different defaults depending on other -e has been specified
        if args.get("little_endian", False):
            self.octets_per_group = 4
        elif self.binary:
            self.octets_per_group = 1
        elif args.get("postscript", False):
            self.octets_per_group = 0
        elif args.get("include", False):
            self.octets_per_group = 0
        else:
            self.octets_per_group = 2

        # check for overrides
        attr_octets_per_group = args.get("octets_per_group", None)
        if attr_octets_per_group is not None:
            try:
                if type(attr_octets_per_group) != int:
                    attr_octets_per_group: int = int(attr_octets_per_group, 0)
                self.octets_per_group = attr_octets_per_group
            except ValueError as e:
                errmsg = f"-o {attr_octets_per_group} is not numeric"
                raise ValueError(errmsg)
            if self.octets_per_group < 0:
                raise ValueError(f"-o {attr_octets_per_group} is not a non-negative integer")

        self.include: bool = args.get("include", False)

        length = args.get("len", None)
        if length is not None:
            try:
                if type(length) != int:
                    length = int(length, 0)
                self.length = length
            except ValueError as e:
                errmsg = f"-l {length} is not numeric"
                raise ValueError(errmsg)
            if self.length < 0:
                raise ValueError(f"{length} is not a non-negative integer")

        self.name: str = args.get("name", None)

        attr_offset = args.get("offset", 0)
        if attr_offset is not None:
            try:
                if type(attr_offset) != int:
                    attr_offset: int = int(attr_offset, 0)
                self.offset = attr_offset
            except ValueError as e:
                errmsg = f"-o {attr_offset} is not numeric"
                raise ValueError(errmsg)
            if self.offset < 0:
                raise ValueError(f"{attr_offset=} is not a non-negative integer")

        self.postscript: bool = args.get("postscript", False)
        self.reverse: bool = args.get("reverse", False)
        self.decimal: bool = args.get("decimal", False)
        self.seek = args.get("seek", 0)
        self.uppercase: bool = args.get("uppercase", False)
        self.version: bool = args.get("version", False)

        self.infile: str = args.get("infile", None)
        if self.infile and not self.infile == '-':
            if not os.path.exists(self.infile):
                raise RuntimeError(f"{self.pname}: {self.infile}: No such file or directory")
        self.outfile: str = args.get("outfile", None)
