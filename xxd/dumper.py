import os
import sys
from abc import ABC, abstractmethod
from io import UnsupportedOperation

from xxd import HexType, COLS


class Dumper(ABC):
    """Base class for hex dumpers of the three formats"""

    def __init__(self, args: dict):
        """Creates a new XXD object with specified options.
        Note that defaults are implemented here by the dictionary 'get(key, default)' approach.
        Incompatible options raise a ValueError.
        """
        self.args = args if args else {}

        # Remaining members are initialized here in alphabetic order.
        # There should be no dependencies on order
        self.autoskip: bool = args.get("autoskip", False)
        self.autoskip_lines = None
        self.autoskip_state = None
        self.binary: bool = self.set_binary(args)
        self.capitalize: bool = args.get("capitalize", False)
        self.cols = self.set_columns(args)
        self.decimal: bool = args.get("decimal", False)
        self.EBCDIC: bool = args.get("EBCDIC", False)
        self.file_offset = None
        self.fpin = None
        self.fpout = None
        self.hextype = self.set_hextype(args)
        self.include: bool = args.get("include", False)
        self.infile = self.set_infile(args)
        self.length = self.set_length(args)
        self.little_endian: bool = self.set_little_endian(args)
        self.name: str = args.get("name", None)
        self.octets_per_group = self.set_octets_per_group(args)
        self.offset = self.set_offset(args)
        self.outfile: str = args.get("outfile", None)
        self.postscript: bool = args.get("postscript", False)
        self.reverse: bool = args.get("reverse", False)
        self.seek = self.set_seek(args)
        self.so_far = None
        self.uppercase: bool = args.get("uppercase", False)
        self.version: bool = args.get("version", False)

    @staticmethod
    def data_format(b, hextype: HexType) -> str:
        """Converts a byte to a hex or binary string"""
        if hextype == HexType.HEX_BITS:
            result = format(b, "08b")
        else:
            result = format(b, "02x")
        return result

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
            if self.reverse:
                self.mainline_reverse()
            else:
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

    def set_binary(self, args) -> bool:
        """Binary option is incompatible with -ps, -i, or -r"""
        binary: bool = args.get("binary", False)
        if binary:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys() and args[other]:
                    raise ValueError("-b option is incompatible with -ps, -i, or -r.")
        return binary

    def set_columns(self, args) -> int:
        """Cols option has different defaults depending on whether -ps or -i have been specified"""
        cols = self.get_default_columns()
        if "cols" in args:  # See if an override was specified
            attr_cols = args.get("cols", None)
            if attr_cols is not None:
                try:
                    if type(attr_cols) != int:
                        attr_cols: int = int(attr_cols, 0)
                    cols = attr_cols
                except ValueError as e:
                    errmsg = f"-c {attr_cols} is not numeric"
                    raise ValueError(errmsg)
                if cols < 0:
                    raise ValueError(f"-c {attr_cols} is not a non-negative integer")
        if cols > COLS:
            raise ValueError(f"Number of columns {cols} cannot be greater than {COLS}")
        return cols

    def set_hextype(self, args):
        """Returns the element of HexType needed for this type of output"""
        hextype = HexType.HEX_NORMAL
        if "postscript" in args:
            hextype = HexType.HEX_POSTSCRIPT
        elif "include" in args:
            hextype = HexType.HEX_CINCLUDE
        elif "binary" in args:
            hextype = HexType.HEX_BITS
        elif "litte_endian" in args:
            hextype = HexType.HEX_LITTLEENDIAN
        return hextype

    def set_infile(self, args):
        """Returns the input file name after checking to ensure the file exists"""
        infile: str = args.get("infile", None)
        if infile and not infile == '-':
            if not os.path.exists(infile):
                pname = os.path.basename(sys.argv[0])
                raise RuntimeError(f"{pname}: {infile}: No such file or directory")
        return infile

    def set_length(self, args):
        """Returns the length attribute as an integer.
        Translated from a hex literal if necessary."""
        length = args.get("len", None)
        if length is None:
            return None
        try:
            if type(length) != int:
                length = int(length, 0)
        except ValueError as e:
            errmsg = f"-l {length} is not numeric"
            raise ValueError(errmsg)
        if length < 0:
            raise ValueError(f"{length} is not a non-negative integer")
        return length

    def set_little_endian(self, args):
        """Returns the value of the little endian option.
        The little endian option is incompatible with -ps, -i, or -r"""
        little_endian: bool = args.get("little_endian", False)
        if little_endian:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-e option is incompatible with -ps, -i, or -r.")
        return little_endian

    def set_octets_per_group(self, args) -> int:
        """Returns the octets per group according to either the
        output type or any override.

        The octets per group option has different defaults depending on
        whether -e has been specified
        """

        # Set the default according to the output type
        octets_per_group = self.get_default_octets_per_group()
        attr_octets_per_group = args.get("octets_per_group", None)
        if attr_octets_per_group is not None:
            try:
                if type(attr_octets_per_group) != int:
                    attr_octets_per_group: int = int(attr_octets_per_group, 0)
                octets_per_group = attr_octets_per_group
            except ValueError as e:
                errmsg = f"-o {attr_octets_per_group} is not numeric"
                raise ValueError(errmsg)
            if octets_per_group < 0:
                raise ValueError(f"-o {attr_octets_per_group} is not a non-negative integer")
        return octets_per_group

    def set_offset(self, args) -> int | None:
        """Sets the offset attribute if specified in the arguments"""
        offset = args.get("offset", None)
        if offset is None:
            return None
        try:
            if type(offset) != int:
                offset = int(offset, 0)
        except ValueError as e:
            errmsg = f"-o {offset} is not numeric"
            raise ValueError(errmsg)
        if offset < 0:
            raise ValueError(f"{offset} is not a non-negative integer")
        return offset

    def set_seek(self, args) -> int | None:
        """Sets the seek attribute if specified in the arguments"""
        seek = args.get("seek", None)
        if seek is None:
            return None
        try:
            if type(seek) != int:
                seek = int(seek, 0)
        except ValueError as e:
            errmsg = f"-s {seek} is not numeric"
            raise ValueError(errmsg)
        if seek < 0:
            raise ValueError(f"{seek} is not a non-negative integer")
        return seek

    @abstractmethod
    def mainline(self):
        """Runs the dumper"""

        self.file_offset = 0
        self.so_far = 0
        if self.seek is not None:
            seek = self.seek
            try:
                self.fpin.seek(seek)
            except UnsupportedOperation as e:
                for i in range(seek):
                    self.fpin.read(1)
            self.file_offset += seek

    @abstractmethod
    def mainline_reverse(self):
        """Recreates original file from the hex output"""

    @abstractmethod
    def get_default_columns(self) -> int:
        """Returns the default number of columns for this output type"""

    @abstractmethod
    def get_default_octets_per_group(self) -> int:
        """Returns the default number of octets per group for this output type"""
