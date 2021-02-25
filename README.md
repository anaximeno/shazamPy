# SHA-ZAM

 Shazam is a **Comand Line Application** made in python that checks the integrity of one file by comparing it with a given hash.
<br>
<br>
It as also other options like:
* calculate all supported hashsums of one file
* read a file with hash sum and filename inside
* calculate only the file sum without compare it 

Prerequesites:
* Python version 3.5.x or higher
* termcolor version 1.1.x or higher (install it with pip or conda)
* alive_progress version 1.6.x or higher (install it with pip or conda)


### How Does Shazam Work ?

It calculates the file's hash sum and compares it with a given hash, if they were equal, it will show a sucess message, else, it will show an unsucess message.

### Usage & More

#### General formula:
	
	$ shazam [COMMAND] [Contents..]


#### Example for only calculating the hash sums(1):

	$ shazam calc sha1 linux.iso freebsd.iso [...]

##### General Formula(1):

	$ shazam calc [*sumtype] [files...]

**Supported sumtypes**: *md5*, *sha1*, *sha224*, *sha256*, *sha384*, *sha512*, can use also the sumtype *all* for getting all supported sumtypes

#### Example checking and comparing hash sum(2):

  	$ shazam check sha1 4fe31ea2ce34ef45234fbedfca linux.iso

##### General formula(2):

	$ shazam check [*sumtype] [filesum] [filename]

*Supported sumtypes: md5, sha1, sha224, sha256, sha384, sha512.

#### Example reading a file with hash sum and filename inside(3):

	$ shazam read sha1sum.txt

##### General formula(3):

	$ shazam read [filename]


**OBS:** For more options, try, after install it:

	$ shazam --help

**I am open to sugestion, so, if you have one send it to me, or make it yourself.**
