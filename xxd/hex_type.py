from enum import Enum


class HexType(Enum):
    """The different hextypes known by this program"""
    HEX_NORMAL = 0
    HEX_POSTSCRIPT = 1
    HEX_CINCLUDE = 2
    HEX_BITS = 3  # not a hex dump, but bits: 01111001
    HEX_LITTLEENDIAN = 4
