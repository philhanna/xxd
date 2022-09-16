import sys

version_string = "xxd 2022-09-16 by Juergen Weigert et al."
os_version = " (win32)" if sys.platform[0:3] == "win" else ""

from .hex_type import HexType
from .hex_dumper import HexDumper

__all__ = [
    'version_string',
    'os_version',
    'HexType',
    'HexDumper',
]