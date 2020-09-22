import os


# checksum "type of check" "file_path"  "original file sum or path"
# reader = ['checksum', 'type of check', 'file_path', 'file sum']
def instruction(inst):
    reader = inst.split()
    state = ['md5', 'sha1', 'sha256']


    def ins0(index): # check the initialization
        if index != "checksum":
            return False
        else:
            return index


    def ins1(index): # check the type of sum
            if index in state:
                return index # fiz assim para evitar o caso de
                                 # colocarem mais de um tipo de sum
            else:
                return False
    

    def ins2(index): # check the existence of the file
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return index
        except IOError:
            return False

    
    def ins3(index): # read the sum file or text
        if not ins2(index):
            return ins2(index)


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
    return ins1(reader[1]), ins2(reader[2]), ins3(reader[3]), ins0(reader[0])

# checksum sha1 testfile.png sha1.txt
