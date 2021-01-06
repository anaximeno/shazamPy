# ShaZam

ShaZam is a **CLI** application made basically in python. <br>
It checks the integrity of one file by comparing it with a given hash.

## General Information

### How does it work

It calculates the file's hash sum and compares it with a given hash, <br>
if they were equal it will show a sucess message, <br>
else it will say that the calculated hash and the given one are different.

### Usage & More
You can use it as below:

  > shazam *-sha1* "*file_name*" "*given_sum*"

**OBS:** If you have a text file with the filename and hash sum wrote inside you can check it using another command. <br>
For more options, try, after install it: shazam -h/--help
  
Types of hash that you can currently calculate and/or check:

* md5
* sha1
* sha224
* sha256
* sha384
* sha512

**If you have suggestions send it to me!**
