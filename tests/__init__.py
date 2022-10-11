"""Unit tests"""
import os.path
import sys
import tempfile
from contextlib import contextmanager

from tests.savedir import SaveDirectory

my_dir = os.path.dirname(__file__)
project_root_dir = os.path.abspath(os.path.join(my_dir, ".."))
testdata = os.path.join(project_root_dir, "testdata")
tmp = tempfile.gettempdir()


# redirect stdout technique from https://www.python.org/dev/peps/pep-0343/

@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


@contextmanager
def stderr_redirected(new_stderr):
    save_stderr = sys.stderr
    sys.stderr = new_stderr
    try:
        yield None
    finally:
        sys.stderr = save_stderr


@contextmanager
def stdin_redirected(new_stdin):
    save_stdin = sys.stdin
    sys.stdin = new_stdin
    try:
        yield None
    finally:
        sys.stdin = save_stdin


__all__ = [
    'tmp',
    'SaveDirectory',
    'project_root_dir',
    'testdata',
    'stdout_redirected',
    'stderr_redirected',
    'stdin_redirected',
]
