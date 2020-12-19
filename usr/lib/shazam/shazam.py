#!/usr/bin/python3
''' shazam 2020.1
Calculates the file sum and compares it with an given sum
Author: Anaxímeno Brito
'''

# TODO: put one decorator below (or more)
# TODO: must check if the imports of all modules are working well, if not, mssss

import sys
import argparse

from common import Process, hlist, out_error, CheckVars


def main():
    parser = argparse.ArgumentParser(
        description="Check and Compare the sums.",
        usage="shazam [OPTION] content...",
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
        option.add_argument("-%s" % item, "--%ssum" % item, metavar='')  # metavar is empty

    args = parser.parse_args()

    def make_process(givensum, sumtype, filename):
        procs = Process(filename=filename, sumtype=sumtype, givensum=givensum)

        if givensum:
            procs.normal()

            if args.verbose:
                procs.verbose()

        else:
            print("It will only show the file's %s!" % sumtype)
            procs.only_sum()

    if args.version:
        with open("/usr/share/shazam/VERSION", "rt") as f:
            print("ShaZam: %s" % str(f.read()))
    elif args.file:
        if args.content:
            checks = CheckVars(filename=args.content, givensum=None)
            found, unfounded = checks.analyze_text()
            if found:
                fname, gsum, stype = found[0]
                procs = Process(filename=fname, sumtype=stype, givensum=gsum)
                procs.normal()
            else:
                out_error("None of these file(s) was/were found:", exit=False)
                for unf in unfounded:
                    print("*", unf)
                sys.exit(1)
        else:
            parser.error("expected one argument")
    elif args.Files:
        if args.content:
            checks = CheckVars(filename=args.content, givensum=None)
            found, unfounded = checks.analyze_text()
            if found:
                for i in range(len(found)):
                    fname, gsum, stype = found[i]
                    procs = Process(filename=fname, givensum=gsum, sumtype=stype)
                    procs.normal()
                if unfounded:
                    print("The file(s) below was/were not found:")
                    for unf in unfounded:
                        print("* ", unf)
            else:
                print("None of the file(s) below was/were found:")
                for unf in unfounded:
                    print("* ", unf)
        else:
            parser.error("expected one argument")
    elif args.all:
        if args.content:
            procs = Process(args.content)
            procs.allsums()
        else:
            out_error("expected one argument")
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
            procs = Process(args.content)
            procs.allsums()
        else:
            out_error("Aborted!\nusage: shazam [OPTION] content...")
    else:
        out_error("No options was chosen, \ntry: shazam -h, for more informations.")

if __name__ == '__main__':
    main()
