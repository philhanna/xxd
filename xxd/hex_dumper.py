import sys

from xxd import HexType


class HexDumper:
    """Hex dumper"""

    def __init__(self, args: dict):
        """Creates a new XXD object with specified options.
        Note that defaults are implemented here by the dictionary 'get(key, default)' approach.
        Incompatible options raise a ValueError.
        """
        self.pname: str = sys.argv[0].split("/")[-1]
        self.autoskip: bool = args.get("autoskip", False)

        # Binary option is incompatible with -ps, -i, or -r
        self.binary: bool = args.get("binary", False)
        if self.binary:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-b option is incompatible with -ps, -i, or -r.")

        self.capitalize: bool = args.get("capitalize", False)

        # Cols option has different defaults depending on whether -ps or -i have been specified
        if "postscript" in args:
            self.cols = 30
        elif "include" in args:
            self.cols = 12
        else:
            self.cols = 16

        self.EBCDIC: bool = args.get("EBCDIC", False)

        # Little endian option is incompatible with -ps, -i, or -r
        self.little_endian: bool = args.get("little_endian", False)
        if self.little_endian:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-e option is incompatible with -ps, -i, or -r.")

        # Octets per group option has different defaults depending on other -e has been specified
        if "little_endian" in args:
            self.octets_per_group = 4
        else:
            self.octets_per_group = 2

        self.include: bool = args.get("include", False)
        length = args.get("len", None)
        if length is not None:
            if str(length).isdigit():
                length = int(length)
                if length < 0:
                    raise ValueError(f"{length} is not a non-negative integer")
            else:
                raise ValueError(f"{length} is not numeric")
        self.length: int = length
