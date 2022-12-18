from pathlib import Path

import pytest

from tests import tmp


@pytest.fixture
def file1():
    return Path(tmp).joinpath("file1")


@pytest.fixture
def file2():
    return Path(tmp).joinpath("file2")
