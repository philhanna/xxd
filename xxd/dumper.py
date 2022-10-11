import sys
from abc import ABC, abstractmethod


class Dumper(ABC):
    """Base class for hex dumpers of the three formats"""

    def __init__(self, args: dict):
        self.args = args
        self.reverse = None
        self.outfile = None
        self.infile = None
        self.pname: str = sys.argv[0].split("/")[-1]
        self.fpin = None
        self.fpout = None
        self.so_far = None
        self.file_offset = None

    @abstractmethod
    def mainline(self):
        """Runs the dumper"""
        pass

    @abstractmethod
    def mainline_reverse(self):
        """Recreates original file from the hex output"""
        pass

    def run(self):
        """Calls mainline with specified input and output files"""

        # Check for infile.  If not specified, or if it is "-", use stdin.
        # Otherwise, try to open the file.
        # If outfile is specified, open it for writing, otherwise, use stdout.

        self.fpin = None
        self.fpout = None
        try:
            if self.infile is None or self.infile == sys.stdin or self.infile == '-':
                self.fpin = sys.stdin
            else:
                self.fpin = open(self.infile, "rb")

            if self.outfile is None or self.outfile == sys.stdout:
                self.fpout = sys.stdout
            else:
                self.fpout = open(self.outfile, "wb")

            # Run the mainline
            if self.reverse:
                self.mainline_reverse()
            else:
                self.mainline()

        # Close the files
        finally:
            if self.fpin is not None:
                if self.fpin != sys.stdin:
                    self.fpin.close()
            if self.fpout is not None:
                self.fpout.flush()
                if self.fpout != sys.stdout:
                    self.fpout.close()
