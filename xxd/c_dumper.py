import string

from xxd import Dumper


class CDumper(Dumper):
    """Works with C include format"""

    def __init__(self, args):
        super().__init__(args)

    def get_default_columns(self) -> int:
        return 12

    def get_default_octets_per_group(self) -> int:
        return 0

    def mainline(self):
        super().mainline()  # Important!

        # Function used within this block that writes either
        # a string or bytes. This avoids having to write the
        # logic in every self.fpout.write() in this block.
        def write_line(line):
            try:
                self.fpout.write(line)
            except TypeError:
                line = bytes(line.encode("utf-8"))
                self.fpout.write(line)

        # Print the C array heading
        varname = self.infile if not self.name else self.name

        # Ensure that this is a valid C variable name
        varname = CDumper.convert_to_valid_c_variable_name(varname)

        if self.capitalize:
            varname = varname.upper()

        # The varname is now cifyied
        line = f"unsigned char {varname}[] = {{" + "\n"
        write_line(line)
        self.fpout.flush()

        # Read bytes and write them as hex literals,
        # writing output lines at every self.cols boundary
        # and at end of file
        n = 0
        cinc = []
        c = self.fpin.read(1)
        while len(c) > 0:
            if self.length is not None:
                if n >= self.length:
                    break
            n += 1
            hex_literal = "0x" + format(ord(c), "02x")
            cinc.append(hex_literal)
            if n % self.cols == 0:
                line = "  " + ", ".join(cinc)
                cinc.clear()
                write_line(line)
            c = self.fpin.read(1)
            if n % self.cols == 0:
                if len(c) == 0:
                    write_line("\n")
                else:
                    if hasattr(self, 'length') and self.length == n:
                        write_line("\n")
                    else:
                        write_line(",\n")
        if len(cinc) > 0:
            line = "  " + ", ".join(cinc)
            write_line(line + "\n")
        write_line("};\n")
        self.fpout.flush()

        # Now write array length
        varname_len = f"{varname}_len"
        if self.capitalize:
            varname_len = varname_len.upper()
        line = f"unsigned int {varname_len} = {n};\n"
        write_line(line)
        self.fpout.flush()

    def mainline_reverse(self):
        raise RuntimeError("-r option is not supported for C include files")

    @staticmethod
    def convert_to_valid_c_variable_name(varname):
        if varname[0].isdigit():
            varname = "__" + varname
        valid = []
        for c in varname:
            if c in string.ascii_letters or c in string.digits or c == "_":
                valid.append(c)
            else:
                valid.append("_")
        varname = "".join(valid)
        return varname
