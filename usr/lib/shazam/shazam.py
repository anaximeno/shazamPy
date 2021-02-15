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
		self.process = Process()

	def make_process(self):
		"""Performs specific processing depending on the arguments."""
		if self.args.type:
			self.process.define_sumtype(self.args.type)

			if self.args.content:
				filename, givensum = self.args.content
				self.process.add_file(FileId(filename, givensum))
				self.process.check_process()
			elif self.args.files:
				for filename in self.args.files:
					self.process.add_file(FileId(filename))
				self.process.only_show_sum()
				if self.args.write: self.process.write()
			else:
				print_error("Spected more arguments")

		elif self.args.read:
			txt_file = self.args.read[0]
			self.process.define_sumtype(sumtype(txt_file))
			for filename, givensum in contents(txt_file):
				self.process.add_file(FileId(filename, givensum))
			self.process.check_multifiles()

		elif self.args.all:
			self.process.add_file(FileId(self.args.all[0]))
			self.process.show_allsums()

		else:
			print_error('No option was chosen!')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog="shazam",
		description="Checks and Compare the sums.",
		usage="shazam [OPTION] content..."
	)
	parser.add_argument("--version", help="Print the current version of this program.",
						action='version', version='%(prog)s {}'.format(__version__))

	# TODO: Check the help output
	# TODO: Make only write option
	parser.add_argument("--type", choices=sumtypes_list)
	parser.add_argument("--content", nargs=2)
	parser.add_argument("-A", "--all", nargs=1)
	parser.add_argument("-f", "--files", nargs='+')
	parser.add_argument("-r", "--read", nargs=1)
	parser.add_argument("-w", "--write", action='store_true')

	args = parser.parse_args()

	if len(sys.argv) > 1:
		mf = MainFlow(args)
		mf.make_process()

	else:
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
