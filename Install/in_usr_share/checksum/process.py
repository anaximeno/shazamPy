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


# read the sum file or text
def original_sum(index):
    def analyze_file(x):
        def ext(y):
            file_name, file_extension = os.path.splitext(y)
            return file_extension
        if ext(x) == ".txt":
            return True
        else:
            return False
    if analyze_file(index):
        try:
            with open(index, "rt") as m:
                while True:
                    sum_text = m.read()
                    if not sum_text:
                        break
                    return sum_text
        except FileNotFoundError:
            print(f"{index} was not found!")
            return False
    else:
        return index


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
