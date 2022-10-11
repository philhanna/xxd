from xxd import Dumper


class PostscriptDumper(Dumper):
    """Works with postscript format"""

    def __init__(self, args):
        super().__init__(args)

    def mainline(self):
        super().mainline()  # Important!

    def mainline_reverse(self):
        super().mainline_reverse()  # Important!
