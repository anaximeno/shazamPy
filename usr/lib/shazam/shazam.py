#!/usr/bin/python3
""" ShaZam  can calculate a file sum and compare with a given one.

ShaZam as also other options like:
	calculate all supported hashsums of one file
	calculate and compare file sum which is inside a text file
	Calculate only the file sum without compare it 

Prerequesites:
	Python version 3.2.x or higher
	termcolor version 1.1.x or higher (install it with pip or conda)
	alive_progress version 1.6.x or higher (install it with pip or conda)
"""

### Libraries
# Standart Libraries
import sys
import argparse

# Support Module
from common import *


__author__ = "Anaxímeno Brito"
__version__ = version
__license__ = "GNU General Public License v3.0"
__copyright__ = "Copyright (c) 2021 by Anaxímeno Brito"


# TODO: Make an option to save the output in one file
class MainFlow(object):
	"""Organizes the program's processing flow."""

	def __init__(self, args):
		self.args = args
		self.subarg = args.subparser

	def make_process(self):
		"""Performs specific processing depending on the arguments."""
		if self.subarg:
			if self.subarg == 'check':
				process = Process(
					[FileId(self.args.filename, self.args.filesum)], 
					sumtype=self.args.sumtype
				)
				process.checkfile()
			elif self.subarg == 'calc':
				process = Process(
					[FileId(fname) for fname in self.args.files],
					sumtype=self.args.sumtype
				)
				process.show_sum()
				if self.args.write: process.write()
			elif self.subarg == 'read':
				process = Process(
					[FileId(fname, fsum) for fsum, fname in contents(self.args.filename)],
					sumtype=get_sumtype(self.args.filename)
				)
				process.checksum_plus()
			elif self.subarg == 'all':
				process = Process(
					[FileId(self.args.filename)]
				)
				process.totalcheck()

		else:
			print_error('No option was chosen!')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog="shazam",
		description="Checks and Compare the file hashsums.",
	)
	parser.add_argument("--version", help="Print the current version of this program.",
						action='version', version='%(prog)s {}'.format(__version__))
	subparser = parser.add_subparsers(dest='subparser')

	# Positional arguments for check and compare hashsums
	check = subparser.add_parser('check')
	check.add_argument("sumtype", choices=sumtypes_list)
	check.add_argument("filesum")
	check.add_argument("filename")

	# Positional arguments for only calculate hashsums
	calc = subparser.add_parser('calc')
	calc.add_argument('sumtype', choices=sumtypes_list)
	calc.add_argument("-w", "--write", action='store_true')
	calc.add_argument('files', nargs='+')

	# Positional arguments for read a file which
	# has the file sum and names wrote in.
	read = subparser.add_parser('read')
	read.add_argument('filename')

	# Postional arguments for calculating all
	# sums of the file
	all_sums = subparser.add_parser('all')
	all_sums.add_argument('filename')

	# Get all arguments
	args = parser.parse_args()

	if len(sys.argv) > 1:
		mf = MainFlow(args)
		mf.make_process()

	else:
		print("usage: shazam [-h] [--version] {check,calc,read,all} ...")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
 
