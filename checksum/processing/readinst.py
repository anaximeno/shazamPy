# Author: Anaximeno Brito
# Calculates the file sum and compares it with an given sum
# September 2020 - currently

from .hashes import hashes as hashlist
import os
from .output import OutPut


sumslist = {}

op = OutPut()

for item in hashlist:
    sumslist[item + "sum"] = item
    sumslist[item + "sums"] = item


def is_readable(file):
    if exists(file):
        try:
            with open(file, "rt") as f:
                f.read(1)
                return True
        except UnicodeDecodeError:
            op.out_error(f"{file} is unreadable, must be a file with the sums and filename inside!")
            return False
    else:
        op.out_error(f"{file} do not exits in this dir!")


# check the existence of the file
def exists(file):
    try:
        with open(file, 'rb') as target:
            if target:
                return True
    except IOError:
        return False


# check if the value is an hexadecimal value
def _hex(hexa):
    try:
        int(hexa, 16)
        return True
    except ValueError:
        return False

def type_of_sum(text):
    if is_readable(text):
        text_path = text.split('/')
        otxt = text_path[len(text_path) -1]
        sum_name = os.path.splitext(otxt)[0]
        if sum_name in sumslist:
            return sumslist[sum_name]
        else:
            tp = ''
            for item in sumslist:
                tp += '\n ' + item

            op.out_error(f"'{sum_name}' is unsupported already!")
            print("'-f' and '-F' method uses the file name to specify the type of sum that should be used," +
                  f" so the file name actually supported are: {tp}")
            return False

class CheckVars:

    def __init__(self, fname, hash):
        self.file = fname
        self.hashSum = hash

    # analyze the existence and the sum conditions
    def analyze_file(self):
        if exists(self.file) and _hex(self.hashSum):
            return True
        elif not exists(self.file):
            op.out_error(f"'{self.file}' was not found here in this directory!")
        elif not _hex(self.hashSum):
            op.out_error(f"'{self.hashSum}' is not an hexadecimal number!")

    # analyze the content of the sum.txt given
    def analyze_text(self):
        if not type_of_sum(self.file):
            return False, False
        try:
            file_base = {}
            with open(self.file, "rt") as t:
                try:
                    line = 0
                    for l in t:
                        line += 1
                        file_sum, file_name = l.split()
                        if _hex(file_sum):
                            file_base[file_name] = file_sum
                        else:
                            op.out_error(f"irregularity in the line {line} of '{self.file}', " +
                                  f"sum must be an hexadecimal value!")
                            return False, False
                except ValueError:
                    op.out_error(f"'{self.file}' must have the file sum and the file name in each line!")
                    print(f"Irregularity in line {line}")
                    return False, False

                unfounded = []
                found = []

                def find_files(file):
                    if exists(file):
                        found.append((file, file_base[file], type_of_sum(self.file)))
                    else:
                        unfounded.append(file)

                for f in file_base:
                    find_files(f)

                return found, unfounded
        except FileNotFoundError:
            op.out_error(f"'{self.file}' was not found!")
            return False, False
