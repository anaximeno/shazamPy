from process import get_data, results
from readinst import instruction, erros

help = '''

        *Usage: checksum -hash [file path] [file/hash sum]

        *Types of hash that you can currently use:
            -md5
            -sha1
            -sha224
            -sha256
            -sha384
            -sha512

        *If you are in the file_to_be_checked's path you can just write the file's file_name

        *In [file/hash sum] you can use an file(.txt) that currently has the sum or the sum code/text itself

        *EXAMPLE:*
            -> checksum -sha1 testfile.png sha1.txt
     '''

try:
    # read the instructions of the input
    readed = instruction(input(' -> '))

    stop_check = False

    #check if we get all the data from instructions
    for i in range(3):
        if not readed[i]:
            stop_check = True
            break

    if not stop_check:
        tipo = readed[0]
        fdir = readed[1]
        fsum = readed[2]

        print("") # jump one line
        print('-' * 65)

        get_data(fdir, tipo)
        results(tipo, fsum)

        print('-' * 65)
        print("") # jump one line

        print("")
    else:
        print("")
        print(f' %Err: {erros[0]} , check if you folowed the usage as below.' + help)
except IndexError:
    print('''
            Bad Syntax!

    Usage: checksum [type of check] [file path] [file sum]

    ''')


# checksum "type of check" "file_path" "original file sum or path"
# checksum sha1 testfile.png sha1.txt
