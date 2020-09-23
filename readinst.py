import os
from process import hashlist

erros = []

# checksum "type of check" "file_path"  "original file sum or path"
# reader = ['checksum', 'type of check', 'file_path', 'file sum']
def instruction(inst):
    reader = inst.split()

    # check the if the first word == checksum
    def ini_call(index):
        if index != "checksum":
            return False
        else:
            return index

    # check the type of sum
    def sum_type(index):
            if index in hashlist:
                return index
            else:
                erros.append(f"{index} hash sum type was not regognized!")
                return False

    # check the existence of the file
    def file_exists(index):
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return index
        except IOError:
            erros.append(f"{index} was not found")
            return False

    # read the sum file or text
    def original_sum(index):
        def analyze_file(x):
            def ext(y):
                file_name, file_extension = os.path.splitext(y)
                return file_extension
            if ext(x) == ".txt":
                needTo = True
            else:
                needTo = False
            return needTo
        if analyze_file(index) is True:
            try:
                with open(index, "rt") as m:
                    while True:
                        sum_text = m.read()
                        if not sum_text:
                            break
                        return sum_text
            except FileNotFoundError:
                erros.append(f"{index} was not found!")
                return False
        else:
            return index



    # return the values for the processment
    return sum_type(reader[1]), file_exists(reader[2]), original_sum(reader[3]), ini_call(reader[0])

# checksum sha1 testfile.png sha1.txt
