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
        args = args if args else {}
        self.args = args

        self.seek = None
        self.reverse = None
        self.outfile = None
        self.infile = None
        self.pname: str = sys.argv[0].split("/")[-1]
        self.fpin = None
        self.fpout = None
        self.so_far = None
        self.file_offset = None
        self.autoskip: bool = args.get("autoskip", False)
        self.autoskip_lines = None
        self.autoskip_state = None
        self.hextype = HexType.HEX_NORMAL
        self.binary: bool = self.set_binary(args)
        self.capitalize: bool = args.get("capitalize", False)
        self.cols = self.set_columns(args)
        self.EBCDIC: bool = args.get("EBCDIC", False)
        self.little_endian: bool = self.set_little_endian(args)
        self.include: bool = args.get("include", False)
        self.length = self.set_length(args)
        self.name: str = args.get("name", None)
        self.octets_per_group = self.set_octets_per_group(args)
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
        if args.get("seek") is None:
            args["seek"] = None
        self.seek = args.get("seek", None)
        if self.seek is None:
            self.seek = 0
        elif type(self.seek) != int:
            self.seek = int(self.seek, 0)
        self.uppercase: bool = args.get("uppercase", False)
        self.version: bool = args.get("version", False)

        self.infile: str = args.get("infile", None)
        if self.infile and not self.infile == '-':
            if not os.path.exists(self.infile):
                raise RuntimeError(f"{self.pname}: {self.infile}: No such file or directory")
        self.outfile: str = args.get("outfile", None)

    def data_format(self, b):
        result = None
        if self.hextype == HexType.HEX_BITS:
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
            self.hextype = HexType.HEX_BITS
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

    def set_length(self, args):
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
        """Little endian option is incompatible with -ps, -i, or -r"""
        little_endian: bool = args.get("little_endian", False)
        if little_endian:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-e option is incompatible with -ps, -i, or -r.")
        return little_endian

    def set_octets_per_group(self, args) -> int:
        """Octets per group option has different defaults depending on other -e has been specified"""
        octets_per_group = self.get_default_octets_per_group()
        if args.get("little_endian", False):
            octets_per_group = 4
        elif self.binary:
            octets_per_group = 1
        elif args.get("postscript", False):
            octets_per_group = 2
        elif args.get("include", False):
            octets_per_group = 0
        else:
            octets_per_group = 2
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

    @abstractmethod
    def mainline(self):
        """Runs the dumper"""

        self.file_offset = 0
        self.so_far = 0
        if self.seek:
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
        pass

    @abstractmethod
    def get_default_columns(self) -> int:
        pass

    @abstractmethod
    def get_default_octets_per_group(self) -> int:
        pass
