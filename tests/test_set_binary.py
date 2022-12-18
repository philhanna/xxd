import pytest
from xxd import Dumper


def test_bogus():
    args = {"binary": "bogus"}
    with pytest.raises(ValueError) as ve:
        Dumper.set_binary(args)
    errmsg = str(ve.value)
    assert "is not True or False" in errmsg


def test_default():
    assert not Dumper.set_binary({})


def test_false():
    assert not Dumper.set_binary({"binary": False})


def test_true():
    assert Dumper.set_binary({"binary": True})
