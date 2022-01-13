#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = "GNU General Public License v3.0"
__version__ = '1.0.0a'
__author__ = 'Anaxímeno Brito'
__copyright__ = "Copyright (c) 2020-2021 by " + __author__


from common import  get_hashtype_from_filename, get_hashtype_from_string_length
from common import File, TextFile, Process, ShazamWarningHandler
import argparse
import sys


class MainFlow(object):
	"""Organizes the program's processing flow."""

	__slots__ = ["args", "subarg", "_process"]
	def __init__(self, args):
		self.args = args
		self._process = Process()

		if not args.subparser:
			err = ShazamWarningHandler(halt=True, value=1)
			err.add("subcommands were not given!")

		self.subarg = args.subparser

	def make_process(self):
		"""Performs specific processing depending on the arguments."""
		if self.subarg == 'check':
			hashtype = self.args.type or get_hashtype_from_string_length(self.args.HASH_SUM)
			if hashtype is None:
				err = ShazamWarningHandler(halt=True)
				err.add('the hash type was not recognized, please specify it using -t/--type <TYPE>'
					f'Available Hash Types: {", ".join(Process.HASHTYPES_LIST)}'
				)
			self._process.checkfile(
				file=File(self.args.FILE, self.args.HASH_SUM),
				hashtype=hashtype, verbosity=self.args.verbose)
		elif self.subarg == 'calc':
			files = [File(fname) for fname in self.args.FILES]
			if self.args.type != 'all':
				self._process.calculate_hash_sum(
					files=files, verbosity=self.args.no_verbose,
					hashtype=self.args.type)
				if self.args.write:
					self._process.write(files, self.args.type, self.args.name)
			else:
				self._process.totalcheck(files)
		elif self.subarg == 'read':
			t = TextFile(self.args.filename)
			contents = t.get_content()

			if not any(contents):
				e = ShazamWarningHandler(halt=True)
				e.add(f'{self.args.filename!r} is empty!')
			elif len(contents) == 1:
				self._process.checkfile(
					file=File(*contents[0]),
					hashtype=self.args.type or get_hashtype_from_filename(self.args.filename),
					verbosity=self.args.verbose)
			else:
				self._process.checkfiles(
					files=[File(*file_attrs) for file_attrs in contents],
					hashtype=self.args.type or get_hashtype_from_filename(self.args.filename),
					verbosity=self.args.verbose)


def get_args():
	hash_types = Process.HASHTYPES_LIST+['all']

	parser = argparse.ArgumentParser(
		prog="shazam",
		usage='%(prog)s {sub-command}',
		epilog='SHAZAM - %s' % __copyright__
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
		description="Verifies the integrity of the file.",
		usage='shazam check <HASH_SUM> <FILE> {--type/-t <HASH_TYPE>}'
	)
	check.add_argument("-t", "--type", help=f"The type of hash sum, it must be one these: {Process.HASHTYPES_LIST}",
		choices=Process.HASHTYPES_LIST, metavar='TYPE')
	check.add_argument("HASH_SUM", help="file's hash sum")
	check.add_argument("FILE", help="file's full or relative location")
	check.add_argument("-V", "--verbose", action='store_true')
	# Positional arguments for only calculate hashsums
	calc = subparser.add_parser('calc',
		help='calculates and show the hash sum',
		usage='shazam calc {-t/--type} <FILES> (...)',
		description='Calculates and show the hash sum.'
	)
	calc.add_argument("-t", "--type", help=f"The type of hash sum, it must be one these: {hash_types}",
		choices=hash_types, metavar='TYPE', required=True)
	calc.add_argument("-w", "--write", action='store_true',
		help='Saves all calculated hash sums inside one file'
	)
	calc.add_argument("--no-verbose", "--noverbose", action='store_false')
	calc.add_argument('-n', '--name', metavar='NAME',
		help='Use this with the argument --write for determining the file\'s name.'
	)
	calc.add_argument('FILES', nargs='+',
		help="One or more files for calculating the hash sums"
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
	read.add_argument('-V', '--verbose', action='store_true', help="verbose option")
	read.add_argument('-t', '--type', metavar='', choices=Process.HASHTYPES_LIST,
		help='This can be used to specify the hashtype if it was not recognized in the file\'s name.'
	)

	return parser.parse_args()


if __name__ == '__main__':
	# If there are more than one arguments it will execute the program else send the usage message to the user
	if len(sys.argv) > 1:
		args = get_args()
		MainFlow(args).make_process()
		ShazamWarningHandler.unstack_all()
	else:
		print("usage: shazam [-h] [--version] {Sub-Command}")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
