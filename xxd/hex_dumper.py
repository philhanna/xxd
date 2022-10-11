import os.path
import re

from xxd import HexType, COLS, ebcdic_table, Dumper


class HexDumper(Dumper):
    """Python version of Juergen Weigert's xxd"""

    def __init__(self, args):
        super().__init__(args)

    def get_default_columns(self) -> int:
        cols = 6 if self.binary else 16
        return cols

    def get_default_octets_per_group(self) -> int:
        if self.args.get("little_endian", False):
            octets_per_group = 4
        elif self.binary:
            octets_per_group = 1
        else:
            octets_per_group = 2
        return octets_per_group

    def mainline(self):
        """Runs the hex dumper"""

        super().mainline() # Important!

        self.autoskip_lines = []
        self.autoskip_state = 0
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

            # Handle normal output

            data_list = [
                data[i: i + self.octets_per_group: 1]
                for i in range(0, len(data), self.octets_per_group)
            ]

            hex_list = [
                "".join([self.data_format(b) for b in chunk_bytes])
                for chunk_bytes in data_list
            ]

            text_list = [
                "".join([self.text_format(b) for b in chunk_bytes])
                for chunk_bytes in data_list
            ]

            sdata = " ".join(hex_list)
            if self.cols % 2 == 1:
                sdata += " "
            if self.uppercase:
                sdata = sdata.upper()
            text = "".join(text_list)
            offset_shown = self.file_offset
            if hasattr(self, "offset"):
                if self.offset is not None:
                    if type(self.offset) != int:
                        self.offset = int(self.offset, 0)
                    add_offset = self.offset
                    offset_shown += add_offset
            if self.decimal:
                offset_format_str = "08d"
            else:
                offset_format_str = "08x"

            group_width = {
                HexType.HEX_BITS: 8,
                HexType.HEX_NORMAL: 4
            }.get(self.hextype, 4)
            n_groups = int(self.cols / self.octets_per_group)
            data_width = (1 + group_width) * n_groups  # Add 1 for the space separator
            line = f"{offset_shown:{offset_format_str}}: {sdata:{data_width}s} {text}\n"

            if not self.autoskip:
                self.xxd_line(line)
            else:
                self.xxd_line_autoskip(line, sdata)

            # Done with normal output

            self.file_offset += chunk_size
            self.so_far += len(data)
            if hasattr(self, "length"):
                length = self.length
                if self.so_far >= length:
                    break

        if self.autoskip:
            if self.autoskip_state == 0:
                pass
            elif self.autoskip_state == 1:
                self.xxd_line(self.autoskip_lines[0])
            elif self.autoskip_state == 2:
                self.xxd_line(self.autoskip_lines[0])
                self.xxd_line(self.autoskip_lines[1])
            elif self.autoskip_state == 3:
                self.xxd_line(self.autoskip_lines[0])
                self.xxd_line("*\n")
                self.xxd_line(self.autoskip_lines[-1])

    def mainline_reverse(self):
        """Reconstructs the original file"""
        if self.seek:
            for i in range(self.seek):
                self.fpout.write(b'\x00')

        for line in self.fpin.readlines():

            # Convert to string
            line = str(line)

            # Skip the offset
            p = line.find(": ")
            if p < 0:
                continue
            line = line[p + 2:]

            # Skip the text
            q = line.find("  ")
            if q < 0:
                continue
            line = line[0:q]

            # Get the hex pairs, convert to characters, and write to output
            hex_pairs = [int(hex_pair, 16)
                         for hex_pair
                         in re.findall("[0-9a-fA-F]{2}", line)]
            for c in hex_pairs:
                b = bytes([c])
                try:
                    self.fpout.write(b)
                except TypeError:
                    ch = chr(c)
                    self.fpout.write(ch)

    def text_format(self, c: int):
        if self.EBCDIC:
            c = ebcdic_table[c]
        if c < 128 and chr(c).isprintable():
            return chr(c)
        else:
            return "."

    def xxd_line(self, line):
        bline = line.encode('utf-8')
        try:
            self.fpout.write(bline)
        except TypeError as e:
            self.fpout.write(line)
        self.fpout.flush()

    def xxd_line_autoskip(self, line: str, sdata: str):
        sdata = sdata.replace(" ", "")
        allzero = all([c == "0" for c in sdata])

        if self.autoskip_state == 0:
            if allzero:
                if len(self.autoskip_lines) == 0:
                    self.autoskip_lines.append(line)
                else:
                    self.xxd_line(self.autoskip_lines[0])
                    self.autoskip_lines.clear()
                    self.xxd_line("*\n")
                    self.autoskip_lines.append(line)
                self.autoskip_state = 1
            else:
                self.xxd_line(line)
                self.autoskip_state = 0

        elif self.autoskip_state == 1:
            if allzero:
                self.autoskip_lines.append(line)
                self.autoskip_state = 2
            else:
                self.xxd_line(self.autoskip_lines[0])
                self.xxd_line(line)
                self.autoskip_state = 0

        elif self.autoskip_state == 2:
            if allzero:
                self.autoskip_lines.append(line)
                self.autoskip_state = 3
            else:
                self.xxd_line(self.autoskip_lines[0])
                self.xxd_line(self.autoskip_lines[1])
                self.autoskip_lines.clear()
                self.xxd_line(line)
                self.autoskip_state = 0

        elif self.autoskip_state == 3:
            if allzero:
                self.autoskip_lines.append(line)
                self.autoskip_state = 3
            else:
                self.xxd_line(self.autoskip_lines[0])
                self.xxd_line("*\n")
                self.autoskip_lines.clear()
                self.xxd_line(line)
                self.autoskip_state = 0
