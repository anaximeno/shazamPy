# Author: Anaximeno Brito
# Calculates the file sum and compares it with an given sum
# September 2020 - currently

import os
from time import sleep
from .readinst import CheckVars, exists
from .hashes import hashes as hashlist
from .output import OutPut
from alive_progress import alive_bar
from termcolor import colored

# don't ever change this number
BUF_SIZE = 32768

op = OutPut()


# this is used in the function below to gen data
def gen(dt):
    if dt:
        yield dt


# read all sums
def all_sums(f_name):
    with alive_bar(len(hashlist), bar='blocks', spinner='dots') as bar:
        for s_type in hashlist:
            with open(f_name, 'rb') as f:
                while True:
                    try:
                        file_data = gen(f.read(BUF_SIZE))
                        hashlist[s_type].update(next(file_data))
                        # when lower is this value, faster will be the reading,
                        sleep(0.00001)
                        # but it will use more CPU
                    except StopIteration:
                        break
            bar()


# read and set the file's sum
def readata(f_name, s_type):
    size = os.path.getsize(f_name)
    times = 0

    while size > 0:
        size -= BUF_SIZE
        times += 1

    with alive_bar(times, bar='filling', spinner='dots') as bar:
        with open(f_name, 'rb') as f:
            while True:
                try:
                    file_data = gen(f.read(BUF_SIZE))
                    hashlist[s_type].update(next(file_data))
                    # when lower is this value, faster will be the reading,
                    sleep(0.00001)
                    # but it will use more CPU
                    bar()
                except StopIteration:
                    break
                


# it checks if the file's sum is equal to the given sum
def check(file_sum, sum_type, file_name):
    h = hashlist[sum_type].hexdigest()

    op = OutPut(
        fname=file_name,
        stype=sum_type,
        hsum=file_sum
    )

    if int(h, 16) == int(file_sum, 16):
        op.out_results(sucess=True)
    else:
        op.out_results(sucess=False)


class Process:

    def __init__(self, fileName, sumType=None, hashSum=None):
        self.file = fileName
        self.sumType = sumType
        self.hashSum = hashSum

    # if we have the file's name and sum
    def normal(self):
        cv = CheckVars(fname=self.file, hash=self.hashSum)

        if cv.analyze_file():
            readata(self.file, self.sumType)
            check(self.hashSum, self.sumType, self.file)

    # if the file's name and sum is in a sum.txt file
    def text(self):

        cv = CheckVars(fname=self.file, hash=None)

        found, unfounded = cv.analyze_text()

        if found:
            f_name, f_sum, s_type = found[0]

            readata(f_name, s_type)
            check(f_sum, s_type, f_name)
        else:
            op.out_error("None of these file(s) was/were found:")
            for unf in unfounded:
                print("*", unf)

    # get all sums
    def allsums(self):
        if exists(self.file):
            all_sums(self.file)
            output = ""
            for typo in hashlist:
                h = hashlist[typo].hexdigest()
                output += f" {typo}sum: {h}\n"
            print(f"\nAll '{self.file}' sums below: ")
            print(output)
        else:
            op.out_error(f"'{self.file}' was not found!")

    # if we want only show the sum and no to compare it
    def only_sum(self):
        if exists(self.file):
            readata(self.file, self.sumType)
            print(f"'{self.file}' {self.sumType}sum is: {hashlist[self.sumType].hexdigest()}")
        else:
            op.out_error(f"'{self.file}' was not found!")

    def multi_files(self):
        cv = CheckVars(fname=self.file, hash=None)

        found, unfounded = cv.analyze_text()

        if found:
            for i in range(len(found)):
                f_name, f_sum, s_type = found[i]

                readata(f_name, s_type)
                check(f_sum, s_type, f_name)
            if unfounded:
                print(f"The file(s) below was/were not found:")
                for unf in unfounded:
                    print("*", unf)
        else:
            print("None of the file(s) below was/were found:")
            for unf in unfounded:
                print("*", unf)

    def verbose(self):
        op = OutPut(
            fname=self.file,
            stype=self.sumType,
            hsum=self.hashSum
        )
        op.verbose()
