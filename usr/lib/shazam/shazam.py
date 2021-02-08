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


try :
	with open("/usr/share/shazam/VERSION", "rt") as ver :
		vers = str(ver.read()).strip()

except FileNotFoundError :
	vers = 'Undefined'


__author__ = "Anaxímeno Brito"
__version__ = vers
__license__ = "GNU General Public License v3.0"
__copyright__ = "Copyright (c) 2021 by Anaxímeno Brito"


import sys
from common import Process, Analyze, FileId, Out


try :
	import argparse

except ImportError :
	Out.error("Important Module is not installed yet: argparse",
			  "\nInstall it with: pip/pip3 install argparse")


class MainFlow :

	def __init__(self, args) :
		self.args = args
		self.process = Process()

	def make_process(self) :
		"""Analysis command args and make specified process"""
		if self.args.type :
			self.process.define_sumtype(self.args.type)
			
			if self.args.content :
				filename, givensum = self.args.content

				self.process.add_file(FileId(filename, givensum))
				self.process.check_process()

			elif self.args.files :
				for filename in self.args.files :
					self.process.add_file(FileId(filename))
				self.process.only_show_sum()

			else :
				Out.error("Spected more arguments")

		elif self.args.read :
			txt_file = self.args.read[0]
			self.process.define_sumtype(Analyze.sumtype(txt_file))

			for filename, givensum in Analyze.contents(txt_file).items() :
				self.process.add_file(FileId(filename, givensum))

			self.process.check_multifiles()

		elif self.args.all :
			self.process.add_file(FileId(self.args.all[0]))
			self.process.show_allsums()

		else :
			Out.error('No option was chosen!')
			

if __name__ == '__main__' :
	parser = argparse.ArgumentParser(
		prog="ShaZam",
		description="Checks and Compare the sums.",
		usage="shazam [OPTION] content..."
	)
	parser.add_argument("--version", help="Print the current version of this program.", action='version', version='%(prog)s {}'.format(__version__))

	# TODO: Check the help output
	parser.add_argument("--type", choices=Analyze.sumtypes_list)
	parser.add_argument("--content", nargs=2)
	parser.add_argument("-A", "--all", nargs=1)
	parser.add_argument("-f", "--files", nargs='+')
	parser.add_argument("-r", "--read", nargs=1)

	args = parser.parse_args()


	if len(sys.argv) > 1 :
		mf = MainFlow(args)
		mf.make_process()

	else :
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
