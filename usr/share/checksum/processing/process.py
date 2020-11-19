# Author: Anaximeno Brito
# Calculates the file sum and compares it with an given sum
# 2020
# TODO: must use decorators, and lambda

import os
from .readinst import CheckVars, exists
from .hashes import hashes as hashlist
from .output import OutPut
from time import sleep
from alive_progress import alive_bar
from termcolor import colored

# don't change this number
BUF_SIZE = 32768

op = OutPut()
cv = CheckVars()

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
                        data = gen(f.read(BUF_SIZE))
                        hashlist[s_type].update(next(data))
                        # when lower is this value, faster will be the reading,
                        sleep(0.00001)
                        # but it will use more CPU
                    except StopIteration:
                        break
            bar()


# read and set the file's sum
def readata(f_name, s_type):

    def rep(s):
        t = 0
        while s > 0:
            s -= BUF_SIZE
            t += 1
            yield t

    size = os.path.getsize(f_name)
    times = 0
    for x in rep(size):
        times = x

    with alive_bar(times, bar='filling', spinner='dots') as bar:
        with open(f_name, 'rb') as f:
            while True:
                try:
                    data = gen(f.read(BUF_SIZE))
                    hashlist[s_type].update(next(data))
                    # when lower is this value, faster will be the reading,
                    sleep(0.00001)
                    # but it will use more CPU
                    bar()
                except StopIteration:
                    break


# it checks if the file's sum is equal to the given sum
def check(file_sum, sum_type, file_name):
    x = int(file_sum, 16)
    h = hashlist[sum_type].hexdigest()

    if int(h, 16) == x:
        suc = True
    else:
        suc = False

    op.results(
        fname=file_name, 
        stype=sum_type, 
        hsum=file_sum,
        sucess=suc
    )

    op.out_message()


class Process():

    def __init__(self, file=False, sumType=False, hashSum=False):
        self.file = file
        self.sumType = sumType
        self.hashSum = hashSum

    # if we have the file's name and sum
    def normal(self):

        cv.set_file(self.file)
        cv.set_hash_sum(self.hashSum)

        if cv.analyze_file():
            readata(self.file, self.sumType)
            check(self.hashSum, self.sumType, self.file)

    # if the file's name and sum is in a sum.txt file
    def text(self):

        cv.set_file(self.file)

        found, unfounded = cv.analyze_text()
        
        if found:
            f_name, f_sum, s_type = found[0]

            readata(f_name, s_type)
            check(f_sum, s_type, f_name)
        else:
            op.out_error("None of these file(s) was/were found:")
            for f in unfounded:
                print(" ", f)

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
        cv.set_file(self.file)

        found, unfounded = cv.analyze_text()

        if found:
            for i in range(len(found)):
                f_name, f_sum, s_type = found[i]

                readata(f_name, s_type)
                check(f_sum, s_type, f_name)
            if unfounded:
                print(f"The file(s) below was/were not found:")
                for f in unfounded:
                    print(" ", f)
        else:
            print("None of the file(s) below was/were found:")
            for f in unfounded:
                print(colored(f" {f}", "red"))

    def verbose(self):

        op.results(
            fname=self.file, 
            stype=self.sumType, 
            hsum=self.hashSum,
            sucess=None
        )

        op.verbose()
