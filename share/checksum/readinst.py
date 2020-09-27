import os
from process import hashlist


def check_vars(stype, fdir, fsum):

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
                return False

    # check the existence of the file
    def file_exists(index):
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return True
        except IOError:
            print(f"\nFile {index} was not found")
            return False

    # check if the value is an hexadecimal value
    def analyze_hex(hexa):
        try:
            int(hex, 16)
            return True
        except ValueError:
            print(f"{hexa} is not an hexadecimal value!")
            return False

    
    # return the values for the processment
    return sum_type(stype) * file_exists(fdir) * analyze_hex(fsum)
