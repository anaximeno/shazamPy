import os

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
        print(f"{hexa} is not an hexadecimal value!")
        return False

# analyze the existence and the sum conditions
def analyze_file(f_name, f_sum):
    if exists(f_name) and _hex(f_sum):
        return True
    elif not exists(f_name):
        print(f"{f_name} wasn't found here!")
    elif not _hex(f_sum):
        print(f"{f_sum} is not an hexadecimal number, must be an hexadecimal number!")

# analyze the content of the sum.txt given
def analyze_text(text):
    try:
        fileBase = {}
        with open(text, "rt") as t:
            try:
                for line in t:
                    file_sum, file_name = line.split()
                    fileBase[file_name] = file_sum
            except ValueError:
                print(f'{text} must have the file sum and the file name in each line!')
                return False, False
            notFound = []
            for files in fileBase:
                if exists(files):
                    return files, fileBase[files]
                elif not exists(files):
                    notFound.append(files)
                    if len(notFound) == len(fileBase):
                        nfound = ""
                        for nf in notFound:
                            nfound += "\n " + nf
                        print(f'None of these file(s) below was found in this directory: {nfound}')
                        return False, False
    except FileNotFoundError:
        print(f"{text} was not found!")
        return False, False
