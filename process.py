import sys
import hashlib
import os

hashlist = {
  "md5": hashlib.md5(),
  "sha1": hashlib.sha1(),
  "sha224": hashlib.sha224(),
  "sha256": hashlib.sha256(),
  "sha384": hashlib.sha384(),
  "sha512": hashlib.sha512()
}


def file_exists(index):
        try:
            f = open(index, 'rb')
            f.read()
            f.close()
            return True
        except IOError:
            print(f"\nFile {index} was not found")
            return False
            
# read the sum file or text
def original_sum(index):
    def analyze_file(x):
        def ext(y):
            file_name, file_extension = os.path.splitext(y)
            return file_extension
        if ext(x) == ".txt":
            return True
        else:
            print(f'{x} is not an .txt file!')
            return False, False
    if analyze_file(index):
        fileBase = {}
        try:
            with open(index, "rt") as m:
                for line in m:
                  file_sum, file_name = line.split()
                  fileBase[file_name] = file_sum
            for file in fileBase:
              if file_exists(file):
                return file, fileBase[file]
              else:
                continue
        except FileNotFoundError:
            print(f"{index} was not found!")
            return False, False
    else:
        return False, False


def get_data(file, tipo):
  BUF_SIZE = 32768
  with open(file, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      elif tipo in hashlist:
        hashlist[tipo].update(data)
      else:
        print(f'ERRor: {tipo} is not in the hashlist!')
        break


def results(tipo, fsum):
  x = int(fsum, 16)
  if tipo in hashlist:
      if int(hashlist[tipo].hexdigest(), 16) == x:
        print(f"  #SUCESS, the {tipo}sum did match!")
      else:
        print(f"  %FAIL, the {tipo}sum didn't match!")
  else:
      print(f"ERRor: {tipo} is unknown!")
