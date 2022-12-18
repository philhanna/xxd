import pytest
from xxd import HexDumper, CDumper, PostscriptDumper


@pytest.mark.parametrize("attrname,expected", [
    ("autoskip", False),
    ("cols", 16),
    ("octets_per_group", 2),
    ("include", False),
    ("infile", None),
    ("length", None),
    ("name", None),
    ("offset", None),
    ("outfile", None),
    ("seek", None),
    ("EBCDIC", False),
])
def test_defaults(attrname, expected):
    """Default values of XXD attributes"""
    xxd = HexDumper({})
    assert getattr(xxd, attrname) == expected


@pytest.mark.parametrize("parms,substring", [
    ({"binary": True, "include": True}, "incompatible"),
    ({"binary": True, "postscript": True}, "incompatible"),
    ({"binary": True, "reverse": True}, "incompatible"),
    ({"little_endian": True, "include": True}, "incompatible"),
    ({"little_endian": True, "postscript": True}, "incompatible"),
    ({"little_endian": True, "reverse": True}, "incompatible"),
    ({"len": "bogus"}, "not numeric"),
    ({"len": "-1"}, "negative"),
    ({"offset": "bogus"}, "numeric"),
    ({"offset": "-86"}, "negative"),
])
def test_substring_in_errmsg(parms, substring):
    """Tests for incompatible options"""
    with pytest.raises(ValueError) as err:
        HexDumper(parms)
    errmsg = str(err.value)
    assert substring in errmsg


@pytest.mark.parametrize("parms,attrname,expected", [
    ({"autoskip": True}, "autoskip", True),
    ({"binary": True}, "cols", 6),
    ({"decimal": True}, "decimal", True),
    ({"binary": True}, "octets_per_group", 1),
    ({"little_endian": True}, "octets_per_group", 4),
    ({"postscript": True}, "octets_per_group", 2),
    ({"infile": "/usr/bin/cut"}, "infile", "/usr/bin/cut"),
    ({"infile": "-"}, "infile", "-"),
    ({"len": "13"}, "length", 13),
    ({"len": "0"}, "length", 0),
    ({"name": "wonderful"}, "name", "wonderful"),
    ({"offset": 0x100}, "offset", 256),
    ({"postscript": True}, "postscript", True),
    ({"reverse": True}, "reverse", True),
    ({"seek": 0x0100}, "seek", 256),
    ({"uppercase": True}, "uppercase", True),
    ({"version": True}, "version", True),
])
def test_hexdumper_setters(parms, attrname, expected):
    xxd = HexDumper(parms)
    assert getattr(xxd, attrname) == expected


def test_postscriptdumper():
    assert PostscriptDumper({"postscript": True}).cols == 30


def test_cdumper():
    assert CDumper({"include": True}).cols == 12
