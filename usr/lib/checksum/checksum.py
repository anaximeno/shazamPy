'''
Calculates the file sum and compares it with an given sum

Author: Anaxímeno Brito
'''

# TODO: put one decorator below (or more)
# TODO: must check if the imports of all modules are working well, if not, mssss

import argparse

from common import Process, hlist, out_error


def main():
    parser = argparse.ArgumentParser(
        description="Check and Compare the sums.",
        usage="checksum [OPTION] content...",
        epilog="Author: Anaximeno Brito, <anaximenobrito@gmail.com>"
    )

    option = parser.add_mutually_exclusive_group()
    option.add_argument("-f", "--file",
                        help="Check the sum of only one file which have the name and sum wrote in the file.",
                        action="store_true")
    option.add_argument("-F", "--Files",
                        help="Check the sum of all files which have the name and sum wrote in the file.",
                        action="store_true")
    option.add_argument("-A", "--all", help="Print all the file's sums.",
                        action="store_true")
    option.add_argument("-v", "--version", help="Print the current version of this app.", action="store_true")

    parser.add_argument("content", help="file name or sum depending of the choice", nargs='?', default=None)
    parser.add_argument("--verbose", help="Verbose response", action="store_true")

    for item in hlist['type']:
        option.add_argument(f"-{item}", f"--{item}sum", metavar='')  # metavar is empty

    args = parser.parse_args()

    def make_process(givensum, sumtype, filename):
        prc = Process(
            filename=filename,
            sumtype=sumtype,
            givensum=givensum
        )

        if givensum:
            prc.normal()

            if args.verbose:
                prc.verbose()

        else:
            print("It will only show the file's %s!" % sumtype)
            prc.only_sum()

    prc = Process(filename=args.content)

    if args.version:
        with open("/usr/share/checksum/VERSION", "rt") as f:
            print("Checksum:", str(f.read()))
    elif args.file:
        if args.content:
            prc.text()
        else:
            parser.error("expected one argument")
    elif args.Files:
        if args.content:
            prc.multi_files()
        else:
            parser.error("expected one argument")
    elif args.all:
        if args.content:
            prc.allsums()
        else:
            parser.error("expected one argument")
    elif args.md5sum:
        make_process(args.content, "md5", args.md5sum)
    elif args.sha1sum:
        make_process(args.content, "sha1", args.sha1sum)
    elif args.sha224sum:
        make_process(args.content, "sha224", args.sha224sum)
    elif args.sha256sum:
        make_process(args.content, "sha256", args.sha256sum)
    elif args.sha384sum:
        make_process(args.content, "sha384", args.sha384sum)
    elif args.sha512sum:
        make_process(args.content, "sha512", args.sha512sum)
    elif args.content:  # must be the penultimate
        want_all = input(f"Do you want to check all '{args.content}' sums? [Y/n]: ")
        if not want_all or want_all.isspace() or want_all.lower() == "yes" or want_all.lower() == "y":
            print("")  # skip one line
            prc.allsums()
        else:
            print("Aborted!")
            print("usage: checksum [OPTION] content...")
            print("or: checksum -h, for more information.")
    else:
        out_error("No options was chosen, try: checksum -h, for more information.")


main()
