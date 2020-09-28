def __initial__(var):
    import sys
    import process
    from readinst import check_vars

    # list of hashes usables
    hashlist = process.hashlist
    t = ""
    for i in hashlist:
        t += "\n " + i

    help = f'''
Usage: checksum [hash_type] [file path] [hash sum]
Or:    checksum [hash_type] -f [hash_sum.txt]

EX.1: checksum sha1 testfile.png 634a24348c8d7a5c78f589356972d3a2b2fcac23
Ex.2: checksum sha1 -f sha1sum.txt

Types of hash that you can currently use: {t}

'''

    try:
        if var[1] == "--help":
            print(help)
        elif var[2] == "-f":
            file, f_sum = process.original_sum(var[3])
            s_type = var[1]
            if file and f_sum:
                while check_vars(s_type, file, f_sum):
                    process.get_data(file, s_type)
                    process.results(s_type, f_sum, file)
                    break
            else:
                pass
        else:
            # read the instructions of the input
            while check_vars(var[1], var[2], var[3]):
                s_type = var[1]
                file = var[2]
                f_sum = var[3]

                process.get_data(file, s_type)
                process.results(s_type, f_sum, file)
                break
    except IndexError:
        print('''
Can't checksum!

Usage: checksum [type of check] [file path] [file sum]
Or:    checksum [hash_type] -f [hash_sum.txt]
    
You can also use for:
    help: --help
    ''')
