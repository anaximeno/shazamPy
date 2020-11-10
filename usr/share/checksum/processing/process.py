# Author: Anaximeno Brito
#
# Calculates the file sum and compares it with an given sum
# 2020

from . import readinst
import os
from .hashes import hashes
from time import sleep
from alive_progress import alive_bar
from termcolor import colored

hashlist = hashes

# don't change this number
BUF_SIZE = 32768


def gen_data(dt):
    if dt:
        yield dt


# read all sums
def all_sums(f_name):
    with alive_bar(len(hashlist), bar='blocks', spinner='dots') as bar:
        for s_type in hashlist:
            with open(f_name, 'rb') as f: 
                while True:
                    try:
                        data = gen_data(f.read(BUF_SIZE))
                        hashlist[s_type].update(next(data))
                        sleep(0.00001)  # when lower is this value, faster will be the reading,
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
                    data = gen_data(f.read(BUF_SIZE))
                    hashlist[s_type].update(next(data))
                    sleep(0.00001)  # when lower is this value, faster will be the reading,
                    # but it will use more CPU
                    bar()
                except StopIteration:
                    break


# check if the file's sum is equal to the given sum
def check(f_sum, s_type, f_name):
    x = int(f_sum, 16)
    h = hashlist[s_type].hexdigest()

    if int(h, 16) == x:
        print(colored(f"#SUCCESS, '{f_name}' {s_type}sum matched!", "green"))
    else:
        print(colored(f"%FAIL, '{f_name}' {s_type}sum did not match!\n", "red"))


class Process():
    
    def __init__(self, file=False, sumType=False, hashSum=False):
        self.file = file
        self.sumType = sumType
        self.hashSum = hashSum

    # if we have the file's name and sum
    def normal(self):
        if readinst.analyze_file(self.file, self.sumType):
            readata(self.file, self.sumType)
            check(self.hashSum, self.sumType, self.file)

    # if the file's name and sum is in a sum.txt file
    def text(self):
        found, unfounded = readinst.analyze_text(self.file)
        if found:
            f_name, f_sum, s_type = found[0]

            readata(f_name, s_type)
            check(f_sum, s_type, f_name)
        else:
            print("None of these file(s) was/were found:")
            for f in unfounded:
                print(" ", f)

    # get all sums
    def allsums(self):
        if readinst.exists(self.file):
            all_sums(self.file)
            output = ""
            for typo in hashlist:
                output += f" {typo}sum: {hashlist[typo].hexdigest()}\n"
            print(f"\nAll '{self.file}' sums below: ")
            print(output)
        else:
            print(f"checksum: error: '{self.file}' was not found!")


    # if we want only show the sum and no to compare it
    def only_sum(self):
        if readinst.exists(self.file):
            readata(self.file, self.sumType)
            print(f"'{self.file}' {self.sumType}sum is: {hashlist[self.sumType].hexdigest()}")
        else:
            print(f"checksum: error: '{self.file}' was not found!")


    def multi_files(self):
        found, unfounded = readinst.analyze_text(self.file)
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
        h = hashlist[self.sumType].hexdigest()
        print(f"\n-> '{self.file}' {self.sumType}sum: {h}")
        print(f"\n-> The given sum: {self.hashSum}")
