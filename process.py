import sys
import hashlib


hashlist = {
  "md5": hashlib.md5(),
  "sha1": hashlib.sha1(),
  "sha224": hashlib.sha224(),
  "sha256": hashlib.sha256(),
  "sha384": hashlib.sha384(),
  "sha512": hashlib.sha512()
  }


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
        print(f'ERRor: {tipo} is not in the hashlist supported!')
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
