# TODO: verbose should not be shown if an error occurs

from termcolor import colored as clr
from .hashes import hashes as hashlist

class OutPut():

    def __init__(self):
        pass

    def results(self, sucess, fname, hsum, stype):
        self.sucess = sucess
        self.fname = fname
        self.hsum = hsum
        self.stype = stype

    def out_error(self, err):
        self.err = err
        print("checksum: error:", err)

    def out_message(self):
        if self.sucess:
            print(clr(f" #SUCCESS, '{self.fname}' {self.stype}sum matched!", "green"))
        else:
            print(clr(f" %FAIL, '{self.fname}' {self.stype}sum did not match!", "red"))
    
    def verbose(self):    
        print(f" -> Given sum: {self.hsum}")
        print(f" -> '{self.fname}' {self.stype}sum: {hashlist[self.stype].hexdigest()}")
