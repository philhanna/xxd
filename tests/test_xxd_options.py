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


def test_autoskip_true():
    assert HexDumper({"autoskip": True}).autoskip


def test_cols_binary():
    xxd = HexDumper({"binary": True})
    expected = 6
    actual = xxd.cols
    assert actual == expected


def test_cols_postscript():
    xxd = PostscriptDumper({"postscript": True})
    expected = 30
    actual = xxd.cols
    assert actual == expected


def test_cols_include():
    xxd = CDumper({"include": True})
    expected = 12
    actual = xxd.cols
    assert actual == expected


def test_decimal():
    assert HexDumper({"decimal": True}).decimal


def test_g_b():
    xxd = HexDumper({"binary": True})
    expected = 1
    actual = xxd.octets_per_group
    assert actual == expected


def test_g_e():
    xxd = HexDumper({"little_endian": True})
    expected = 4
    actual = xxd.octets_per_group
    assert actual == expected


def test_g_ps():
    xxd = HexDumper({"postscript": True})
    expected = 2
    actual = xxd.octets_per_group
    assert actual == expected


def test_infile():
    xxd = HexDumper({"infile": "/usr/bin/cut"})
    expected = "/usr/bin/cut"
    actual = xxd.infile
    assert actual == expected


def test_infile_stdin():
    xxd = HexDumper({"infile": "-"})
    expected = "-"
    actual = xxd.infile
    assert actual == expected


def test_len():
    xxd = HexDumper({"len": "13"})
    expected = 13
    actual = xxd.length
    assert actual == expected


def test_len_zero():
    xxd = HexDumper({"len": "0"})
    expected = 0
    actual = xxd.length
    assert actual == expected


def test_name():
    xxd = HexDumper({"name": "wonderful"})
    expected = "wonderful"
    actual = xxd.name
    assert actual == expected


def test_offset():
    xxd = HexDumper({"offset": 0x100})
    expected = 256
    actual = xxd.offset
    assert actual == expected


def test_postscript():
    assert HexDumper({"postscript": True}).postscript


def test_reverse():
    assert HexDumper({"reverse": True}).reverse


def test_seek():
    xxd = HexDumper({"seek": 0x0100})
    expected = 256
    actual = xxd.seek
    assert actual == expected


def test_uppercase():
    assert HexDumper({"uppercase": True}).uppercase


def test_version():
    assert HexDumper({"version": True}).version
