# CHECKSUM

Checksum is a **terminal program** made in python that checks the integrity of one file by comparing the file hash to the given hash.

## General Infos

### How does it work

* It converts the file to the hash chosen and compares it with the given hash

### Usage

  > checksum "*hash_type*" "*file_path*" "*original_sum*" <br>
  > checksum "*hash_type*" -f "*hash_sum.txt*"
  
The second type of checksum must be called at the same dir of the file which will be checked

Types of hash that you can currently use:

* md5
* sha1
* sha224
* sha256
* sha384
* sha512

**This program is in tests currently, if you have suggestion let me know ;), if you want to contribute go ahead!**

You can talk with me by sending an email to: anaximenobrito@gmail.com

Fonts I've used to study:

* <https://www.tutorialspoint.com/How-to-Find-Hash-of-File-using-Python>
* <https://www.computerhope.com/issues/ch001721.htm>
* <https://www.journaldev.com/32081/get-file-extension-in-python>
* <https://www.kite.com/python/answers/how-to-convert-a-string-to-hex-in-python>
