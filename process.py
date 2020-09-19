import sys
import hashlib


BUF_SIZE = 32768

md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha256 = hashlib.sha256()

def processing(file, tipo):
  with open(file, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      elif tipo == 'a':
        md5.update(data)
      elif tipo == 'b':
        sha1.update(data)
      elif tipo == 'c':
        sha256.update(data)
      else:
        print('ERR: any error ocurred')
        break


def results(tipo, ssum):
  if tipo == 'a':
    if md5.hexdigest() == ssum:
      print(" MD5 check goes well, everything is OK!")
    else:
      print('Sum not matching!')
  elif tipo == 'b':
    if sha1.hexdigest() == ssum:
      print(" SHA1 check goes well, everything is OK!")
    else:
      print('Sum not matching!')  
  elif tipo == 'c':
    if sha256.hexdigest() == ssum:
      print(" SHA256 check goes well, everything is OK!")
    else:
      print('Sum not matching!')
  else:
    print('ERR: Something went wrong!!')