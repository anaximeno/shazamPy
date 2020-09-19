import process

while True:
  ff = input('File path to be checked -> ')
  tp = input('Type of Sum: [a]MD5, [b]SHA1, [c]SHA256 -> ')
  ss = input('Write/paste your Sum text -> ')

  print('-' * 60) # jump one line 
  process.processing(ff, tp)
  process.results(tp, ss)
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
 