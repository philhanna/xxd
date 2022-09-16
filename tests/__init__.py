"""Unit tests"""
import sys
from contextlib import contextmanager


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
    'stdout_redirected',
    'stderr_redirected',
    'stdin_redirected',
]
