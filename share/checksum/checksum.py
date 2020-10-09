import argparse
import process

# list of hashes usable
hashlist = process.hashlist

# get all types of sums
tp = ""
for item in hashlist:
    tp += " " + item


# principal function
def __initial__():
    parser = argparse.ArgumentParser(
        description="Check and Compare the sums.",
        epilog=f"Types of sums allowed: {tp}",
        usage="checksum [OPTION] content"
    )

    option = parser.add_mutually_exclusive_group()

    option.add_argument("-a", "--archive", help="Check from an archive.txt which " +
                                                "have the file's name and sum inside.", action="store_true")
    option.add_argument("-A", "--All", help="Print all the sum of the file",
                        action="store_true")

    parser.add_argument("content", help="file name or sum depending of the choice", nargs='?', default=None)

    for s in hashlist:
        option.add_argument(f"-{s}", f"--{s}sum", metavar="")

    args = parser.parse_args()

    def made_process(ac, st, fn):
        if ac:
            process.normal(st, fn, ac)  # ac == file sum, fn == file name, st == sum type
        else:
            only_sum = input("Do you only want check the sum? [Y/n]: ")
            if not only_sum or only_sum.isspace() or only_sum.lower() == ("yes" or "y"):
                process.only_sum(st, fn)
            else:
                print("Aborted!")
                print("usage: checksum [sumtype] file sum")  # i can make a prompt to get the sum also
                print("or: checksum -h, for more information.")

    if args.archive:
        if args.content:
            process.text(args.content)
        else:
            parser.error("expected one argument")
    elif args.All:
        if args.content:
            process.allsums(args.content)
        else:
            parser.error("expected one argument")
    elif args.md5sum:
        made_process(args.content, "md5", args.md5sum)
    elif args.sha1sum:
        made_process(args.content, "sha1", args.sha1sum)
    elif args.sha224sum:
        made_process(args.content, "sha224", args.sha224sum)
    elif args.sha256sum:
        made_process(args.content, "sha256", args.sha256sum)
    elif args.sha384sum:
        made_process(args.content, "sha384", args.sha384sum)
    elif args.sha512sum:
        made_process(args.content, "sha512", args.sha512sum)
    elif args.content:  # must be the penultimate
        want_all = input("Do you want to check all '{}' sums? [Y/n]: ".format(args.content))
        if not want_all or want_all.isspace() or want_all.lower() == ("yes" or "y"):
            print("")  # jump one line
            process.allsums(args.content)
        else:
            print("Aborted!")
            print("usage: checksum [OPTION] content")
            print("or: checksum -h, for more information.")
    else:
        parser.error("No options was chosen!")
