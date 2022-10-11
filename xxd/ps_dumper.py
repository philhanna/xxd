from xxd import Dumper


class PostscriptDumper(Dumper):
    """Works with postscript format"""

    def __init__(self, args):
        super().__init__(args)

    def mainline(self):
        super().mainline()  # Important!
        while True:
            chunk_size = self.cols
            if hasattr(self, "length"):
                if self.so_far + chunk_size > self.length:
                    chunk_size = self.length % chunk_size
            data = self.fpin.read(chunk_size)
            if len(data) == 0:
                break

            if type(data) == str:
                data = bytes(data.encode("utf-8"))

            line = "".join([self.data_format(b) for b in data]) + "\n"
            try:
                self.fpout.write(line)
            except TypeError:
                self.fpout.write(line.encode('utf-8'))

            self.file_offset += chunk_size
            self.so_far += len(data)
            if hasattr(self, "length"):
                length = self.length
                if self.so_far >= length:
                    break

    def mainline_reverse(self):
        super().mainline_reverse()  # Important!
