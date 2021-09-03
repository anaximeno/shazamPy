# SHAZAM - Check the file's integrity

Shazam is a **Command Line Application** that checks the integrity of the file by comparing it with a given hash.

> Created by: Anaxímeno Brito

## How Does It Work?

It calculates the file's hash sum and compares it with a given hash for checking if the file isn't corrupted, it can also be used for calculating the hash sums and automatically save it inside one file if wanted.

Shazam supports some of the most used hash types.

### Supported hash types:

* md5sum
* sha1sum
* sha224sum
* sha256sum
* sha384sum
* sha512sum

---

## Installation:

Before the installation secure that you've installed all requirements:

* **Python** - version 3.6.x or higher
* **termcolor** - version 1.1.x or higher (install it with pip or conda)
* **tqdm** - version 4.x or higher (install it with pip or conda)

### How to install:

For installing the program run the installation script '**install.sh**' which is on the root directory of this program as shown below:

    $ sudo sh install.sh

Or on the root directory:

	$ sudo cp usr/bin/shazam /usr/bin/
	$ sudo cp usr/lib/shazam -r /usr/lib/

After installing it, see if it is working using the following command:

	$ shazam

## Usage:

	$ shazam {Sub-Commands} [Arguments..]

### For more options, try, after install it:

	$ shazam --help
