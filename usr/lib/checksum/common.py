import os
import sys
import hashlib as hlib

from time import sleep
from alive_progress import alive_bar
from termcolor import colored as clr

# don't ever change this number
BUF_SIZE = 32768

hlist = {
    "type": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
    "hash": [hlib.md5(), hlib.sha1(), hlib.sha224(), hlib.sha256(), hlib.sha384(), hlib.sha512()],
    "othernames": ["md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum"],
    "pluralnames": ["md5sums", "sha1sums", "sha224sums", "sha256sums", "sha384sums", "sha512sums"]
}


def out_error(err, exit=True):
    print("checksum: error:", err)
    if exit:
        sys.exit(1)


class OutPut:

    def __init__(self, filename=None, givensum=None, sumtype=None):
        self.fname = filename
        self.gsum = givensum
        self.stype = sumtype

    def out_results(self, sucess):
        if sucess:
            print(
                clr(f" #SUCCESS, '{self.fname}' {self.stype}sum matched!", "green")
            )
        else:
            print(
                clr(f" %FAIL, '{self.fname}' {self.stype}sum did not match!", "red")
            )

    def verbose(self):
        index = hlist['type'].index(self.stype)
        filesum = hlist['hash'][index].hexdigest()

        print(
            f" -> Given sum: {self.gsum}\n",
            f"-> '{self.fname}' {self.stype}sum: {filesum}"
        )


op = OutPut()
   

# check the existence of the file
def exists(file):
    try:
        with open(file, 'rb') as target:
            if target:
                return True
    except IOError:
        return False
	

def is_readable(file):
    if exists(file):
        try:
            with open(file, "rt") as f:
                f.read(1)
                return True
        except UnicodeDecodeError:
            out_error(f"{file} is unreadable, must be a file with the sums and filename inside!")
            return False
    else:
        out_error(f"{file} do not exits in this dir!")


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
        name = os.path.splitext(otxt)[0]
        if name in hlist["type"]:
            return name
        elif name in hlist["pluralnames"]:
            index = hlist["pluralnames"].index(name)
            return hlist["type"][index]
        elif name in hlist["othernames"]:
            index = hlist["othernames"].index(name)
            return hlist["type"][index]
        else:
            out_error("'{}' was unrecognized as a supported sum type!".format(name))
            return False

        
class CheckVars:

    def __init__(self, filename, givensum):
        self.fname = filename
        self.gsum = givensum

    # analyze the existence and the sum conditions
    def analyze_file(self):
        if exists(self.fname) and _hex(self.gsum):
            return True
        elif not exists(self.fname):
            out_error(f"'{self.fname}' was not found here in this directory!")
        elif not _hex(self.gsum):
            out_error(f"'{self.gsum}' is not an hexadecimal number!")

    # analyze the content of the sum.txt given
    def analyze_text(self):
        if not type_of_sum(self.fname):
            return False, False
        try:
            file_base = {}
            with open(self.fname, "rt") as t:
                try:
                    line = 0
                    for l in t:
                        line += 1
                        givensum, filename = l.split()
                        if _hex(givensum):
                            file_base[filename] = givensum
                        else:
                            out_error(f"irregularity in the line {line} of '{self.fname}', " +
                                         f"sum must be an hexadecimal value!")
                            return False, False
                except ValueError:
                    out_error(f"'{self.fname}' must have the file sum and the file name in each line!")
                    print(f"Irregularity in line {line}")
                    return False, False

                unfounded = []
                found = []

                def find(filename):
                    if exists(filename):
                        found.append((filename, file_base[filename], type_of_sum(self.fname)))
                    else:
                        unfounded.append(filename)

                for item in file_base:
                    find(item)

                return found, unfounded
        except FileNotFoundError:
            out_error(f"'{self.fname}' was not found!")
            return False, False


# this is used in the function below to gen data
def gen(dt):
    if dt:
        yield dt


# read all sums
def all_sums(f_name):
    with alive_bar(len(hlist['type']), bar='blocks', spinner='dots') as bar:
        for item in hlist['type']:
            with open(f_name, 'rb') as f:
                while True:
                    try:
                        file_data = gen(f.read(BUF_SIZE))
                        index = hlist['type'].index(item)
                        filesum = hlist['hash'][index]
                        filesum.update(next(file_data))
                        # when lower is this value, faster will be the reading,
                        # but it will increase CPU usage
                        sleep(0.00001)
                    except StopIteration:
                        break
            bar()


# read and set the file's sum
def readata(filename, sumtype):
    size = os.path.getsize(filename)
    times = 0

    while size > 0:
        size -= BUF_SIZE
        times += 1

    with alive_bar(times, bar='filling', spinner='dots') as bar:
        with open(filename, 'rb') as f:
            while True:
                try:
                    file_data = gen(f.read(BUF_SIZE))
                    index = hlist['type'].index(sumtype)
                    filesum = hlist['hash'][index]
                    filesum.update(next(file_data))
                    # when lower is this value, faster will be the reading,
                    # but it will increase CPU usage
                    sleep(0.00001)
                    bar()
                except StopIteration:
                    break


# it checks if the file's sum is equal to the given sum
def check(givensum, sumtype, filename):
    index = hlist['type'].index(sumtype)
    filesum = hlist['hash'][index].hexdigest()
    op = OutPut(
        filename=filename,
        sumtype=sumtype,
        givensum=givensum
    )
    if int(filesum, 16) == int(givensum, 16):
        op.out_results(sucess=True)
    else:
        op.out_results(sucess=False)


class Process:

    def __init__(self, filename, sumtype=None, givensum=None):
        self.fname = filename
        self.stype = sumtype
        self.gsum = givensum
        self.checks = CheckVars(filename=self.fname, givensum=self.gsum)

    # if we have the file's name and sum
    def normal(self):
        if self.checks.analyze_file():
            readata(self.fname, self.stype)
            check(self.gsum, self.stype, self.fname)

    # if the file's name and sum is in a sum.txt file
    def text(self):
        found, unfounded = self.checks.analyze_text()
        if found:
            fname, gsum, stype = found[0]
            readata(fname, stype)
            check(gsum, stype, fname)
        else:
            out_error("None of these file(s) was/were found:", exit=False)
            for unf in unfounded:
                print("*", unf)
            sys.exit(1)

    # get all sums
    def allsums(self):
        if exists(self.fname):
            all_sums(self.fname)
            print(f"\nAll '{self.fname}' sums below: ")
            for item in hlist['type']:
                index = hlist['type'].index(item)
                filesum = hlist['hash'][index].hexdigest()
                print(" -> {}sum: {}".format(item, filesum))
        else:
            out_error(f"'{self.fname}' was not found!")

    # if we want only show the sum and no to compare it
    def only_sum(self):
        if exists(self.fname):
            readata(self.fname, self.stype)
            index = hlist['type'].index(self.stype)
            filesum = hlist['hash'][index].hexdigest()
            print(f"'{self.fname}' {self.stype}sum is: {filesum}")
        else:
            out_error(f"'{self.fname}' was not found!")
    
    # TODO: use multi_files funct with recusion on normal funct
    def multi_files(self):
        cv = CheckVars(filename=self.fname, givensum=None)

        found, unfounded = cv.analyze_text()

        if found:
            for i in range(len(found)):
                f_name, f_sum, s_type = found[i]
                readata(f_name, s_type)
                check(f_sum, s_type, f_name)
            if unfounded:
                print(f"The file(s) below was/were not found:")
                for unf in unfounded:
                    print("->", unf)
        else:
            print("None of the file(s) below was/were found:")
            for unf in unfounded:
                print("->", unf)

    def verbose(self):
        op = OutPut(
            filename=self.fname,
            sumtype=self.stype,
            givensum=self.gsum
        )
        op.verbose()
