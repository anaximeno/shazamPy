from process import *
from readinst import instruction

while True:
  readed = instruction(input(' -> ')) # read the instruction
  # get the data
  tp = readed[0]
  fp = readed[1]
  ss = set_file(readed[2])

  print('-' * 60) # jump one line

  get_data(fp, tp)
  results(tp, ss)

  print('-' * 60) # jump another line

  q = input('Do you wanna continue? [Y/n] -> ').lower()
  if q == 'n' or q == 'no':
    break
  else:
    continue

# file to testing below
# file_to_check = 'testfile_original.png' #SHA1 = 634a24348c8d7a5c78f589356972d3a2b2fcac23
                                          #MD5 = 4c5858561a6dcc461a6103d0ab5c1b43
                                          #SHA256 = 07f58a47af48e10ea501ae827784fe51b1433adf70ae16ec9cba3da6884376fe

# checksum "type of check" "file_path" "original file sum or path"
