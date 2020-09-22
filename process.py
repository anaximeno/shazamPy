import sys
import hashlib
import os

md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha256 = hashlib.sha256()


def set_file(file):
    def analyze_file(x):
        def ext(y):
            file_name, file_extension = os.path.splitext(y)
            return file_extension
        if ext(x) == ".txt":
            needTo = True
        else:
            needTo = False
        return needTo
    if analyze_file(file) is True:
        with open(file, "rt") as m:
            while True:
                sum_text = m.read()
                if not sum_text:
                    break
                return sum_text
    else:
        return file


def get_data(file, tipo):
  state = {
    "md5": md5,
    "sha1": sha1,
    "sha256": sha256
  }
  BUF_SIZE = 32768
  with open(file, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      for t in state:
          if  t == tipo:
              state[t].update(data)
              break
          else:
              continue
      else:
        print('ERR: any error ocurred')
        break


def results(tipo, ssum):
  x = int(ssum, 16)
  state = {
    "md5": md5,
    "sha1": sha1,
    "sha256": sha256
  }
  for t in state:
      if str(t) == tipo:
          if int(state[t].hexdigest(), 16) == x:
              print(f"SUCESS, {tipo}sum did match!")
          else:
              print(f"FAIL, {tipo}sum didn't match!")
          break
      else:
          continue
  else:
    print('ERR: Something went wrong!!')
