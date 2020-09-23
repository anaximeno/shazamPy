import os


# checksum "type of check" "file_path"  "original file sum or path"
# reader = ['checksum', 'type of check', 'file_path', 'file sum']
def instruction(inst):
    reader = inst.split()
    state = ['md5', 'sha1', 'sha256']


    def ini_call(index): # check the initialization
        if index != "checksum":
            return False
        else:
            return index


    def sum_type(index): # check the type of sum
            if index in state:
                return index # fiz assim para evitar o caso de
                                 # colocarem mais de um tipo de sum
            else:
                return False


    def file_exists(index): # check the existence of the file
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return index
        except IOError:
            return False


    def original_sum(index): # read the sum file or text
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
            with open(index, "rt") as m:
                while True:
                    sum_text = m.read()
                    if not sum_text:
                        break
                    return sum_text
        else:
            return index



    # return the values for the processment
    return sum_type(reader[1]), file_exists(reader[2]), original_sum(reader[3]), ini_call(reader[0])

# checksum sha1 testfile.png sha1.txt
