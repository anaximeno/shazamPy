# SHA-ZAM - Check the file hash sum

Shazam is a **Command Line Application** that checks the integrity of one file by comparing it with a given hash.  

> Created by: Anaxímeno Brito

## How Does It Work: 

It calculates the file's hash sum and compares it with a given hash for checking if the file isn't corrupted, it can also be used for calculating the hash sums and automatically save it inside one file if wanted. 
 
Shazam supports some of the most used hash types.

### Supported hash types:  
* md5sum
* sha1sum 
* sha224sum 
* sha256sum
* sha384sum 
* sha512sum

## Installation:
Before the installation secure that you've installed all requirements. There isn't no builds for installing the program already so you've to manually install the files on your computer.

#### Prerequisites:  
* **Python** - version 3.6.x or higher  
* **termcolor** - version 1.1.x or higher (install it with pip or conda)  
* **alive_progress** - version 1.6.x or higher (install it with pip or conda)

#### See how to install:
For installing the program, you just have to download this repository and put the file '*usr/bin/shazam*' on '*/usr/bin/*' in your computer and put the directory '*urs/lib/shazam*' on '*/usr/lib*'.

#### More detailed:
On this directory:  
  
	$ sudo cp usr/bin/shazam /usr/bin/
	$ sudo cp usr/lib/shazam -r /usr/lib/

Try to see if it is working:
	
	$ shazam

## Usage:

### General formula:
	
	$ shazam {Sub-Commands} [Arguments..]

### If wanted to read and check the sum on a file:

	$ shazam read [filename]

### For more options, try, after install it:

	$ shazam --help
