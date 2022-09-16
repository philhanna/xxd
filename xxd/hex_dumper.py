import sys

from xxd import HexType


class XXD:
    """xxd"""

    def __init__(self, args):
        self._pname: str = sys.argv[0].split("/")[-1]
        self._autoskip: bool = args.autoskip
        self._hextype: HexType = HexType.HEX_NORMAL

    @property
    def pname(self):
        return self._pname

    @property
    def autoskip(self):
        return self._autoskip

    def run(self):
        """Runs the hex dumper"""
        pass
