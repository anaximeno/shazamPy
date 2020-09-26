import os
from process import hashlist


# checksum "type of check" "file_path"  "original file sum or path"
# readed = ['type of check', 'file_path', 'file sum']
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

    def analyze_file(file):
        file_name, file_extension = os.path.splitext(file)
        if file_extension == ".txt":
            return True
        elif not file_extension:
            try:
                int(file_name, 16)
                return True
            except ValueError:
                print(f"{file_name} is not an hexadecimal value!")
                return False
        else:
            print(f"\nCan't read {file}, \nIt must be: A file_sum.txt or the hexadecimal file sum")
            return False

    
    # return the values for the processment
    return sum_type(stype) * file_exists(fdir) * analyze_file(fsum)

# checksum sha1 testfile.png sha1.txt
