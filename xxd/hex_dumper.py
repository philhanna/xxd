import sys

from xxd import HexType


class XXD:
    """Hex dumper"""

    def __init__(self, args: dict):
        """Creates a new XXD object with specified options.
        Note that defaults are implemented here by the
        dictionary 'get(key, default)' approach."""
        self.pname: str = sys.argv[0].split("/")[-1]
        self.autoskip: bool = args.get("autoskip", False)
        self.binary: bool = args.get("binary", False)
        if self.binary:
            for other in ["postscript", "include", "reverse"]:
                if other in args.keys():
                    raise ValueError("-b option is incompatible with -ps, -i, or -r.")

        self.capitalize: bool = args.get("capitalize", False)

    def run(self):
        """Runs the hex dumper"""
        pass
