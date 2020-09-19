import sys
import hashlib

BUF_SIZE = 32768

md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha256 = hashlib.sha256()

## if you wanna check other file from their directory uncomment the text below --
## -- and comment (#) the next code.
# file_to_check = input('Input the file path -> ')
file_to_check = 'testfile_original.png'

with open(file_to_check, 'rb') as f:
  while True:
    data = f.read(BUF_SIZE)
    if not data:
      break
    md5.update(data)
    sha1.update(data)
    sha256.update(data)
print()
print("MD5: {0}".format(md5.hexdigest()))
print("SHA1: {0}".format(sha1.hexdigest()))
print("SHA256: {0}".format(sha256.hexdigest()))
print()

if sha1.hexdigest() == '634a24348c8d7a5c78f589356972d3a2b2fcac23':
  print('SHA1 ok!')
else:
  print('SHA1 failed!')

if md5.hexdigest() == '4c5858561a6dcc461a6103d0ab5c1b43':
  print('MD5 ok!')
else:
  print('MD5 failed!')
