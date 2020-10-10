import os

sumslist = {
    'md5sum': 'md5',
    'sha1sum': 'sha1',
    'sha224sum': 'sha224',
    'sha256sum': 'sha256',
    'sha384sum': 'sha384',
    'sha512sum': 'sha512'
}

tp = ''  # for posterior use
for item in sumslist:
    tp += '\n ' + item + ".txt"


# check the existence of the file
def exists(file):
    try:
        with open(file, 'rb') as target:
            if target:
                return True
            else:
                IOError()
    except IOError:
        return False


# check if the value is an hexadecimal value
def _hex(hexa):
    try:
        int(hexa, 16)
        return True
    except ValueError:
        return False


# analyze the existence and the sum conditions
def analyze_file(f_name, f_sum):
    if exists(f_name) and _hex(f_sum):
        return True
    elif not exists(f_name):
        print(f"checksum: error: '{f_name}' was not found here in this directory!")
    elif not _hex(f_sum):
        print(f"checksum: error: '{f_sum}' is not an hexadecimal number!")


def type_of_sum(text):
    sum_name, file_ext = os.path.splitext(text)
    if file_ext != ".txt":
        print(f"checksum: error: '{text}' extension must be '.txt' to read!")
        return False
    elif sum_name in sumslist:
        return sumslist[sum_name]
    else:
        print(f"checksum: error: '{sum_name}' is unsupported already!")
        print("'-a' method uses the file name to specify the type of sum that should be used," +
              f" so the file name actually supported are: {tp}")
        return False


# analyze the content of the sum.txt given
def analyze_text(text):
    if not type_of_sum(text):
        return False, False, False
    try:
        file_base = {}
        with open(text, "rt") as t:
            try:
                l = 0
                for line in t:
                    l += 1
                    file_sum, file_name = line.split()
                    file_base[file_name] = file_sum
            except ValueError:
                print(f"checksum: error: '{text}' must have the " +
                      f"file sum and the file name in each line!\nIrregularity in line {l}")
                return False, False, False
            not_found = []
            for files in file_base:
                if exists(files):
                    return files, file_base[files], type_of_sum(text)
                elif not exists(files):
                    not_found.append(files)
                    if len(not_found) == len(file_base):
                        nfound = ""
                        for nf in not_found:
                            nfound += "\n -> " + nf
            
                        print(f"checksum: error: None of these '{text}' file(s) " +
                              f"below was found in this directory: {nfound}")
                        return False, False, False
    except FileNotFoundError:
        print(f"checksum: error: '{text}' was not found!")
        return False, False, False

