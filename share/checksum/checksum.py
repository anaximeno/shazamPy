import process
from readinst import sumslist
# list of hashes usables
hashlist = process.hashlist

# get all types of sums
tp = ""
for item in hashlist:
    tp += "\n " + item

help = f'''\r          
Usage: checksum [type_of_check] [file _name/path] [file_sum]
Usage2:checksum -f typesum.txt

EX.1: checksum sha1 testfile.png 634a24348c8d7a5c78f589356972d3a2b2fcac23
Ex.2: checksum -f sha1sum.txt

Types of hash that you can currently use: {tp}

For others features you can use:

    -f => if you have one file with the sums, see Usage2 
    -A => to check and list all type of checksums supported

'''

# principal function
def __initial__(var):
    try:
        if var[1] == "--help":
            print(help)
        elif var[1] == "-f":
            text = var[2]

            process.text_process(text) #

        elif var[1] == '-A':
            f_name = var[2]

            process.allsums_process(f_name)
        else:
            s_type = var[1]
            f_name = var[2]
            f_sum = var[3]
            if s_type in hashlist:
                process.normal_process(s_type, f_name, f_sum) #
            elif s_type in sumslist:
                process.normal_process(sumslist[s_type], f_name, f_sum)
            else:
                print(f"\r'{s_type}' is unsupported already!\nSupported types: {tp}\n\nCan't checksum!!")
    except IndexError:
        print('''\r          
Can't checksum!

Usage: checksum [type_of_check] [file _name/path] [file_sum]
Or:    checksum [hash_type] -f [hash_sum.txt]

You can also use:
    --help => to give you more instructions!
''')
