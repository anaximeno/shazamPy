from process import get_data, results
from readinst import instruction

try:
    readed = instruction(input(' -> ')) # read the instruction

    stop_check = False

    if not stop_check:
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
    else:
        print(''' ERROR!!
        usage: checksum [type of check] [file path] [file sum]

        types of check that you can use: sha1, sha256, md5

        ''')
except IndexError:
    print(''' Bad Syntax!
    
    usage: checksum [type of check] [file path] [file sum]

    ''')


# checksum "type of check" "file_path" "original file sum or path"
# checksum sha1 testfile.png sha1.txt
