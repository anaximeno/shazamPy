import os
from process import hashlist


def check_vars(s_type, file, f_sum):

    # check the type of sum
    def sum_type(index):
        if index in hashlist:
            return True
        else:
            print(f"\n{index} hash type is not supported already!")
            t = ""
            for i in hashlist:
                t += "\n " + i
            print("\nTypes of hash that you can currently use: {}".format(t))
            print('\nCan\'t checksum!')
            return False

    # check the existence of the file
    def file_exists(index):
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return True
        except IOError:
            print(f"\nFile {index} was not found\n\nCan\'t checksum!")
            return False

    # check if the value is an hexadecimal value
    def analyze_hex(hexa):
        try:
            int(hexa, 16)
            return True
        except ValueError:
            print(f"{hexa} is not an hexadecimal value!\n\nCan\'t checksum!")
            return False

    # return the values for the processment
    return sum_type(s_type) * file_exists(file) * analyze_hex(f_sum)
