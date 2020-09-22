

def instruction(inst):
    reader = inst.split()
    state = ['md5', 'sha1', 'sha256']
    if reader[0] != 'checksum':
        print("Error, write: help")
    for x in state:
        if reader[1] == x:
            tp = x; # fiz assim para evitar o caso de
                    # colocarem mais de um tipo de sum
            break
        else:
            tp = False
    fp = reader[2]
    ss = reader[3]
    return tp, fp, ss
# checksum "file_path" "type of check" "original file sum or path"
