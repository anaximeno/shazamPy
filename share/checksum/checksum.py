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
        usage="checksum [OPTION] file"
    )

    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-a", "--archive", help="Check from an archive.txt \
    which have the file's name and sum inside.", metavar="sum.txt")
    parser.add_argument("-A", "--All", help="Print all the sum of the file",
                        metavar="FILE")
    for s in hashlist:
        group.add_argument(f"-{s}", f"--{s}sum", help=f"Check the {s}sum",
                           nargs=2, metavar=("FILE", "SUM"))

    args = parser.parse_args()

    if args.archive:
        process.text(args.archive)
    elif args.All:
        process.allsums(args.All)
    elif args.md5sum:
        sum_type = "md5"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
    elif args.sha1sum:
        sum_type = "sha1"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
    elif args.sha224sum:
        sum_type = "sha224"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
    elif args.sha256sum:
        sum_type = "sha256"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
    elif args.sha384sum:
        sum_type = "sha384"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
    elif args.sha512sum:
        sum_type = "sha512"
        file_name, file_sum = args.sha1sum
        process.normal(sum_type, file_name, file_sum)
