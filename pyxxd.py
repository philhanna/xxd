#! /usr/bin/python

from xxd import XXD

if __name__ == '__main__':
    import argparse

    version = "xxd 2022-01-14 by Juergen Weigert et al."

    parser = argparse.ArgumentParser(description="xxd")
    parser.add_argument("-a", "--autoskip", action="store_true",
                        help="toggle autoskip. A single '*' replaces nul-lines. Default off.")
    parser.add_argument("-b", "--binary", action="store_true",
                        help="binary digit dump (incompatible with -ps,-i,-r). Default hex.")
    parser.add_argument("-C", "--capitalize", action="store_true",
                        help="capitalize variable names in C include file style (-i).")
    parser.add_argument("-c", "--cols",
                        help="format <cols> octets per line. Default 16 (-i: 12, -ps: 30).")
    parser.add_argument("-E", "--EBCDIC", action="store_true",
                        help="show characters in EBCDIC. Default ASCII.")
    parser.add_argument("-e", "--little-endian", action="store_true",
                        help="little-endian dump (incompatible with -ps,-i,-r).")
    parser.add_argument("-g", "--octets-per-group",
                        help="number of octets per group in normal output. Default 2 (-e: 4).")
    parser.add_argument("-i", "--include", action="store_true",
                        help="output in C include file style.")
    parser.add_argument("-l", "--len",
                        help="stop after <len> octets.")
    parser.add_argument("-n", "--name",
                        help="set the variable name used in C include output (-i).")
    parser.add_argument("-o", "--offset",
                        help="add <off> to the displayed file position.")
    parser.add_argument("-ps", "--postscript", action="store_true",
                        help="output in postscript plain hexdump style.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="reverse operation: convert (or patch) hexdump into binary.")
    parser.add_argument("-d", "--decimal", action="store_true",
                        help="show offset in decimal instead of hex.")
    parser.add_argument("-s", "--seek",
                        help="start at <seek> bytes abs. (or +: rel.)infile offset.")
    parser.add_argument("-u", "--uppercase", action="store_true",
                        help="use upper case hex letters.")
    parser.add_argument("-v", "--version", action="store_true",
                        help=f"show version: \"{version}\".")
    parser.add_argument("infile", nargs="?", help="input file name. Default \"-\" for stdin.")
    parser.add_argument("outfile", nargs="?", help="output file name. Default is stdout.")
    args = parser.parse_args()
    print(f"DEBUG: {args}")
    exit()
    xxd = XXD(args)
    xxd.run()