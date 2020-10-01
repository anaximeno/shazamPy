from readinst import exists
import process as p
# list of hashes usables
from process import hashlist

tp = ""
# get all types of sums
for item in hashlist:
    tp += "\n " + item

help = f'''
Usage: checksum [hash_type] [file path] [hash sum]
Or:    checksum [hash_type] -f [hash_sum.txt]

EX.1: checksum sha1 testfile.png 634a24348c8d7a5c78f589356972d3a2b2fcac23
Ex.2: checksum sha1 -f sha1sum.txt

Types of hash that you can currently use: {tp}

'''


def __initial__(var):
    try:
        if var[1] == "--help":
            print(help)
        elif var[2] == "-f":
            s_type = var[1]
            text = var[3]
            if s_type in hashlist:
                p.text_process(s_type, text)
            else:
                print(f"{s_type} is unsupported already!\n\nCan't checksum!!")
        else:
            s_type = var[1]
            f_name = var[2]
            f_sum = var[3]
            if s_type in hashlist:
                p.normal_process(s_type, f_name, f_sum)
            else:
                print(f"{s_type} is unsupported already!\n\nCan't checksum!!")
    except IndexError:
        print('''
Can't checksum!

Usage: checksum [type of check] [file path] [file sum]
Or:    checksum [hash_type] -f [hash_sum.txt]

You can also use for:
    help: --help
''')
