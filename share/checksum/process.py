import sys
import readinst
import hashlib


hashlist = {
    "md5": hashlib.md5(),
    "sha1": hashlib.sha1(),
    "sha224": hashlib.sha224(),
    "sha256": hashlib.sha256(),
    "sha384": hashlib.sha384(),
    "sha512": hashlib.sha512()
}

BUF_SIZE = 32768


# read all sums
def allSums(f_name):
    with open(f_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            for s_type in hashlist:
                hashlist[s_type].update(data)


# read and set the file's sum
def readata(f_name, s_type):
    with open(f_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hashlist[s_type].update(data)


# check is the file's sum is equal to the given sum
def check(f_sum, s_type, f_name):
    x = int(f_sum, 16)
    h = hashlist[s_type].hexdigest()
    if int(h, 16) == x:
        print('\r          ') # skip one line
        print('-' * 65)
        print(f"  #SUCESS, the {s_type}sum did match!")
        print('-' * 65)
        print(f"\n-> '{f_name}' {s_type}sum: {h}")
        print(f"\n-> Match with the given sum: {f_sum}")
    else:
        print('\r          ') # skip one line
        print('-' * 65)
        print(f"  %FAIL, the {s_type}sum didn't match!")
        print('-' * 65)
        print(f"\n-> '{f_name}' {s_type}sum: {h}")
        print(f"\n-> Don't Match with the given sum: {f_sum}")


# if we have the file's name and sum
def normal_process(s_type, f_name, f_sum):
    if readinst.analyze_file(f_name, f_sum):
        readata(f_name, s_type)
        check(f_sum, s_type, f_name)
    else:
        print("\nCan't checksum!!")


# if the file's name and sum is in a sum.txt file
def text_process(text):
    f_name, f_sum, s_type = readinst.analyze_text(text)
    if f_name and f_sum and s_type:
        readata(f_name, s_type)
        check(f_sum, s_type, f_name)
    else:
        print("\nCan't checksum!!")
        

# get all sums
def allsums_process(f_name):
    if readinst.exists(f_name):
        allSums(f_name)
        output = ""
        for tipo in hashlist:
            output +=  f" {tipo}sum: {hashlist[tipo].hexdigest()}\n"
        print(f"\rAll '{f_name}' sums below: ")
        print(output)
    else:
        print(f"\r{f_name} was not found in this directory!\n\nCan't checksum!!")
