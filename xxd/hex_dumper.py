import os.path
import pdb
import string
import sys
from io import UnsupportedOperation

from xxd import HexType, COLS, ebcdic_table


class HexDumper:
    """Python version of Juergen Weigert's xxd"""

    def mainline(self):
        """Runs the hex dumper"""

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

        ################################################################
        # Handle c-include style output
        ################################################################
        if self.include:

            # Function used within this block that writes either
            # a string or bytes. This avoids having to write the
            # logic in every self.fpout.write() in this block.
            def write_line(line):
                try:
                    self.fpout.write(line)
                except TypeError:
                    line = bytes(line.encode("utf-8"))
                    self.fpout.write(line)

            # Print the C array heading
            varname = self.infile if not self.name else self.name

            # Ensure that this is a valid C variable name
            varname = HexDumper.convert_to_valid_c_variable_name(varname)

            if self.capitalize:
                varname = varname.upper()

            # The varname is now cifyied
            line = f"unsigned char {varname}[] = {{" + "\n"
            write_line(line)
            self.fpout.flush()

            # Read bytes and write them as hex literals,
            # writing output lines at every self.cols boundary
            # and at end of file
            n = 0
            cinc = []
            c = self.fpin.read(1)
            while len(c) > 0:
                if hasattr(self, "length"):
                    if n >= self.length:
                        break
                n += 1
                hex_literal = "0x" + format(ord(c), "02x")
                cinc.append(hex_literal)
                if n % self.cols == 0:
                    line = "  " + ", ".join(cinc)
                    cinc.clear()
                    write_line(line)
                c = self.fpin.read(1)
                if n % self.cols == 0:
                    if len(c) == 0:
                        write_line("\n")
                    else:
                        if hasattr(self, 'length') and self.length == n:
                            write_line("\n")
                        else:
                            write_line(",\n")
            if len(cinc) > 0:
                line = "  " + ", ".join(cinc)
                write_line(line + "\n")
            write_line("};\n")
            self.fpout.flush()

            # Now write array length
            line = f"unsigned int {varname}_len = {n};\n"
            write_line(line)
            self.fpout.flush()

            ############################################################
            # Done with C-include operations
            ############################################################
            return

        while True:
            chunk_size = self.cols
            if hasattr(self, "length"):
                if so_far + chunk_size > self.length:
                    chunk_size = self.length % chunk_size
            data = self.fpin.read(chunk_size)
            if len(data) == 0:
                break
            if type(data) == str:
                data = bytes(data.encode("utf-8"))

            # Handle postscript output
            if self.postscript:
                line = ""
                for b in data:
                    b = self.data_format(b)
                    line += b
                try:
                    self.fpout.write(line)
                    self.fpout.write("\n")
                except TypeError:
                    self.fpout.write(line.encode('utf-8'))
                    self.fpout.write("\n".encode('utf-8'))
            else:

                # Handle normal output

                data_list = [
                    data[i : i + self.octets_per_group : 1]
                    for i in range(0, len(data), self.octets_per_group)
                ]

                hex_list = [
                    "".join([self.data_format(b) for b in chunk_bytes])
                    for chunk_bytes in data_list
                ]

                text_list = [
                    "".join([self.text_format(b) for b in chunk_bytes])
                    for chunk_bytes in data_list
                ]

                sdata = " ".join(hex_list)
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

                group_width = {
                    HexType.HEX_BITS: 8,
                    HexType.HEX_NORMAL: 4
                }.get(self.hextype, 4)
                n_groups = int(self.cols / self.octets_per_group)
                data_width = (1 + group_width) * n_groups  # Add 1 for the space separator
                line = f"{offset_shown:{offset_format_str}}: {sdata:{data_width}s} {text}\n"
                bline = line.encode('utf-8')

                try:
                    self.fpout.write(bline)
                except TypeError as e:
                    self.fpout.write(line)
                self.fpout.flush()

                # Done with normal output

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

    def text_format(self, c: int):
        if self.EBCDIC:
            c = ebcdic_table[c]
        if c < 128 and chr(c).isprintable():
            return chr(c)
        else:
            return "."

    @staticmethod
    def convert_to_valid_c_variable_name(varname):
        if varname[0].isdigit():
            varname = "__" + varname
        valid = []
        for c in varname:
            if c in string.ascii_letters or c in string.digits or c == "_":
                valid.append(c)
            else:
                valid.append("_")
        varname = "".join(valid)
        return varname

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

        # C-style includes
        self.include = args.get("include", False)

        # Octets per group option has different defaults depending on other -e has been specified
        if args.get("little_endian", False):
            self.octets_per_group = 4
        elif self.binary:
            self.octets_per_group = 1
        elif args.get("postscript", False):
            self.octets_per_group = 2
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
