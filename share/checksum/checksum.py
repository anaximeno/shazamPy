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

    option = parser.add_mutually_exclusive_group()

    option.add_argument("-a", "--archive", help="Check from an archive.txt which have the file's name and sum inside.",
                        action="store_true")
    option.add_argument("-A", "--All", help="Print all the sum of the file",
                        action="store_true")

    parser.add_argument("file/sum", help="The file name")

    for s in hashlist:
        option.add_argument(f"-{s}", f"--{s}sum", metavar="file sum")

    args = parser.parse_args()

    if args.archive:
        process.text(args.file)
    elif args.All:
        process.allsums(args.file)
    elif args.md5sum:
        sum_type = "md5"
        file_name = args.md5sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    elif args.sha1sum:
        sum_type = "sha1"
        file_name = args.sha1sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    elif args.sha224sum:
        sum_type = "sha224"
        file_name = args.sha224sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    elif args.sha256sum:
        sum_type = "sha256"
        file_name = args.sha256sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    elif args.sha384sum:
        sum_type = "sha384"
        file_name = args.sha384sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    elif args.sha512sum:
        sum_type = "sha512"
        file_name = args.sha512sum
        file_sum = args.file
        process.normal(sum_type, file_name, file_sum)
    else:
        parser.error("No options was chosen!")
