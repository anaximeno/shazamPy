# ShaZam

  ShaZam is a **CLI** application made in python, that checks the integrity of one file <br>
by comparing it with a given hash.
<br>
ShaZam as also other options like:
	* calculate all supported hashsums of one file
	* calculate and compare file sum wich is inside a text file
	* Calculate only the file sum without compare it 

Prerequesites:
	* Python version 3.2.x or higher
	* termcolor version 1.1.x or higher (install it with pip or conda)
	* alive_progress version 1.6.x or higher (install it with pip or conda)
<hr>
### How does it work

  It calculates the file's hash sum and compares it with a given hash, if they were equal,<br>
it will show a sucess message, else, it will show an unsucess message.

### Usage & More
You can use it as below:

  > shazam *-sha1* "*file_name*" "*given_sum*"

**OBS:** For more options, try, after install it: shazam -h/--help
  
Supported hash types:

* md5
* sha1
* sha224
* sha256
* sha384
* sha512

**I am open to sugestion, so, if you have one send it to me, or make it yourself.**
