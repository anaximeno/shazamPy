# Author: Anaximeno Brito
#
# Calculates the file sum and compares it with an given sum
# September 2020

from .hashes import hashes as hashlist
import os


sumslist = {}

for item in hashlist:
    sumslist[item + "sum"] = item
    sumslist[item + "sums"] = item


tp = ''  # for posterior use
for item in sumslist:
    tp += '\n ' + item


def is_readable(file):
    if exists(file):
        try:
            with open(file, "rt") as f:
                f.read(1)
                return True
        except UnicodeDecodeError:
            print(f"checksum: error: {file} is unreadable, must be a file with the sums and filename inside!")
            return False
    else:
        print(f"checksum: error: {file} do not exits in this dir!")


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


# analyze the existence and the sum conditions
def analyze_file(f_name, f_sum):
    if exists(f_name) and _hex(f_sum):
        return True
    elif not exists(f_name):
        print(f"checksum: error: '{f_name}' was not found here in this directory!")
    elif not _hex(f_sum):
        print(f"checksum: error: '{f_sum}' is not an hexadecimal number!")


def type_of_sum(text):
    if is_readable(text):
        text_path = text.split('/')
        otxt = text_path[len(text_path) -1]
        sum_name, file_ext = os.path.splitext(otxt)
        del file_ext  # unnecessary already
        if sum_name in sumslist:
            return sumslist[sum_name]
        else:
            print(f"checksum: error: '{sum_name}' is unsupported already!")
            print("'-f' and '-F' method uses the file name to specify the type of sum that should be used," +
                  f" so the file name actually supported are: {tp}")
            return False


# analyze the content of the sum.txt given
def analyze_text(text): 
    if not type_of_sum(text):
        return False, False
    try:
        file_base = {}
        with open(text, "rt") as t:
            try:
                line = 0
                for l in t:
                    line += 1
                    file_sum, file_name = l.split()
                    if _hex(file_sum):
                        file_base[file_name] = file_sum
                    else:
                        print(f"checksum: error: irregularity in the line {line} of '{text}', " +
                              f"sum must be an hexadecimal value!")
                        return False, False
            except ValueError:
                print(f"checksum: error: '{text}' must have the " +
                      f"file sum and the file name in each line!\nIrregularity in line {line}")
                return False, False

            unfounded = []
            found = []

            def find_files(file):
                if exists(file):
                    found.append((file, file_base[file], type_of_sum(text)))
                else:
                    unfounded.append(file)

            for f in file_base:
                find_files(f)

            return found, unfounded
    except FileNotFoundError:
        print(f"checksum: error: '{text}' was not found!")
        return False, False
