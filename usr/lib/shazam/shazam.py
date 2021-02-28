#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" ShaZam  can calculate a file sum and compare with a given one.
ShaZam as also other options like:
	calculate all supported hashsums of one file
	read a file with hash sum and filename inside
	calculate only the file sum without compare it
Prerequesites:
	python version 3.2.x or higher
	termcolor version 1.1.x or higher (can install it with pip3 or conda)
	alive_progress version 1.6.x or higher (can install it with pip3 or conda)
"""

### Libraries
# Standart Libraries:
import sys
import argparse

# Non Standart, support Module:
import common as cm
from common import FileID, Process


__author__ = "Anaxímeno Brito"
__version__ = cm.version if cm.version else 'Undefined'
__license__ = "GNU General Public License v3.0"
__copyright__ = "Copyright (c) 2020-2021 by " + __author__


class MainFlow(object):
	"""Organizes the program's processing flow."""
	__slots__ = ["args", "subarg"]
	def __init__(self, args):
		self.args = args
		if not args.subparser:
			cm.print_error("No Subcommands were received!")
		self.subarg = args.subparser

	def make_process(self):
		"""Performs specific processing depending on the arguments."""
		if self.subarg == 'check':
			process = Process(
				[FileID(self.args.filename, self.args.filesum)],
				sumtype=self.args.sumtype
			)
			process.checkfile(verbosity=self.args.no_verbose)
		elif self.subarg == 'calc':
			process = Process(
				[FileID(fname) for fname in self.args.files],
				sumtype=self.args.sumtype if self.args.sumtype != 'all' else None
			)
			if self.args.sumtype != 'all':
				process.show_sum(verbosity=self.args.no_verbose)
				if self.args.write: process.write(self.args.name)
			else: process.totalcheck()
		elif self.subarg == 'read':
			content = cm.contents(self.args.filename)
			process = Process(
				[FileID(fname, fsum) for fsum, fname in content],
				sumtype=self.args.type or cm.get_sumtype(self.args.filename)
			)
			if len(content) == 1:
				process.checkfile(verbosity=self.args.verbose)
			else: process.checkfile_plus(verbosity=self.args.verbose)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog="shazam",
		usage='%(prog)s [-h] [--version] {Sub-Command}',
		epilog='SHA-ZAM %s' %__copyright__
	)
	parser.add_argument("--version",
		help="print the current version of this program", action='version',
		version='%(prog)s {}'.format(__version__)
	)

	# Stores all subparsers
	subparser = parser.add_subparsers(dest='subparser', title='Sub Commands')

	# Positional arguments for check and compare hashsums
	check = subparser.add_parser('check',
		help="check and Compare the file's hash sum",
		description="Check and Compare the file's hash sum.",
		usage='shazam check [-h/--help] [--no-verbose] {sumtype} filesum filename'
	)
	check.add_argument("sumtype", choices=cm.sumtypes_list)
	check.add_argument("filesum", help="file's hash sum")
	check.add_argument("filename", help="file's name")
	check.add_argument("--no-verbose",
		action='store_false', help="no verbose option"
	)

	# Positional arguments for only calculate hashsums
	calc = subparser.add_parser('calc',
		help='calculates and show the hash sum',
		usage='shazam calc [-h/--help] [-w/--write] [--no-verbose] {sumtype} [files...]',
		description='Calculates and show the hash sum.'
	)
	# 'calc_choices' is a list which has all sumtypes in it
	# plus another option (all) which we use to calculate all
	# sumtypes/hashtypes simultaneosly.
	calc_choices = cm.sumtypes_list.copy()
	calc_choices.append('all')
	calc.add_argument('sumtype', choices=calc_choices)
	calc.add_argument("-w", "--write", action='store_true',
		help='saves all calculated sums in a file'
	)
	calc.add_argument("--no-verbose",
		action='store_false', help="no verbose option"
	)
	calc.add_argument('-n', '--name', metavar='',
		help='Use this together with write to determine the writefile\'s name'
	)
	calc.add_argument('files', nargs='+',
		help="one or more files for calculating the hash sums"
	)

	# Positional arguments for reading a file which
	# has the file sum and names wrote in.
	read = subparser.add_parser('read',
		help='read a file with hash sum and filename inside',
		description='Read a file with hash sum and filename inside.',
		usage='shazam read [-h/--help] [--verbose] filename'
	)
	read.add_argument('filename',
		help="file to read in, and check the hash sum of the files inside"
	)
	read.add_argument('--verbose',
		action='store_true', help="verbose option"
	)
	read.add_argument('-t', '--type', metavar='', choices=cm.sumtypes_list,
		help='This can be used to specify the sumtype if it was not recognized in the file\'s name.'
	)

	if len(sys.argv) > 1:
		mf = MainFlow(parser.parse_args())
		mf.make_process()
	else:
		print("usage: shazam [-h] [--version] {Sub-Command}")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
