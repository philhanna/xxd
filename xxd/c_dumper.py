from xxd import Dumper


class CDumper(Dumper):
    """Works with C include format"""

    def __init__(self, args):
        super().__init__(args)

    def mainline(self):
        super().mainline()

    def mainline_reverse(self):
        super().mainline_reverse()


