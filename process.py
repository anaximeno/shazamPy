import sys
import hashlib


md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha256 = hashlib.sha256()


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
      elif tipo in state: 
        state[tipo].update(data)
      else:
        print('ERR: any error ocurred')
        break


def results(tipo, fsum):
  x = int(fsum, 16)
  state = {
    "md5": md5,
    "sha1": sha1,
    "sha256": sha256
  }
  if tipo in state:
      if int(state[tipo].hexdigest(), 16) == x:
        print(f"SUCESS, {tipo}sum did match!")
      else:
        print(f"FAIL, {tipo}sum didn't match!")
  else:
      print("Error in process.results()")

