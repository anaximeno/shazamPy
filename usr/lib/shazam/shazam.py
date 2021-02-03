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

import sys
from common import Process, Analyze, FileId, Out

argv_len = len(sys.argv)

try:
	import argparse

except ImportError:
	Out.error("Important Module is not installed yet: argparse",
			  "\nInstall it with: pip/pip3 install argparse")


# TODO: coloca only_sum pa calcula mas de um arquivos 
# (elimina args.content, e usa sys.argv pa get file oh que ca scodjedo opts)
class MainFlow:

	def __init__(self, args):
		self.args = args
		self.process = Process()

		self.options = {
			'md5': (args.md5, args.md5sum),
			'sha1': (args.sha1, args.sha1sum),
			'sha224': (args.sha224, args.sha224sum),
			'sha256': (args.sha256, args.sha256sum),
			'sha384': (args.sha384, args.sha384sum),
			'sha512': (args.sha512, args.sha512sum)
		}

	def make_process(self):
		if self.args.version:
			try:				
				with open("/usr/share/shazam/VERSION", "rt") as ver:
					print("ShaZam", str(ver.read()).strip())

				sys.exit()

			except FileNotFoundError:
				Out.error("VERSION file was not found")

		elif self.args.file:
			self.process.define_sumtype(Analyze.sumtype(self.args.file))
			content = Analyze.contents(self.args.file)

			for fname, gsum in content.items():
				f = FileId(fname, gsum)

				if f.existence is True:
					self.process.add_file(f)
					break

			else:
				print("\nThis/these file(s) wasn't/weren't found:")

				for filename in content.keys(): 
					print("* ", filename)
				
				sys.exit()
			
			self.process.check_process()

		elif self.args.Files:
			self.process.define_sumtype(Analyze.sumtype(self.args.Files))
			content = Analyze.contents(self.args.Files)
			
			for fname, gsum in content.items():
				f = FileId(fname, gsum)
				self.process.add_file(f)

			self.process.check_multifiles()

		elif self.args.all or argv_len == 2:
			if self.args.all:
				fname = self.args.all

			else:
				fname = self.args.content

			f = FileId(fname)
			self.process.add_file(f)
			self.process.show_allsums()
		
		else:
			for stype, option in self.options.items():
				norm, only = option
				if norm:
					if Analyze.is_hex(norm[0]):
						gsum, fname = norm
		
					elif Analyze.is_hex(norm[1]):
						fname, gsum = norm
		
					else:
						if Analyze.exists(norm[0]):
							Out.error(f"Given sum not recognized: {norm[1]!r}")
		
						elif Analyze.exists(norm[1]):
							Out.error(f"Given sum not recognized: {norm[0]!r}")
		
						else:
							Out.error(f"File given hashsum was not recognized as hexadecimal: {norm[0], norm[1]}")

					f = FileId(fname, gsum)
					self.process.add_file(f)
					self.process.define_sumtype(stype)
					self.process.check_process()
					break
		
				elif only:
					if type(only) is list:
						for item in only:
							f = FileId(item)
							self.process.add_file(f)
							self.process.define_sumtype(stype)
							self.process.only_show_sum()
							break

					else:
						f = FileId(only)
						self.process.add_file(f)
						self.process.define_sumtype(stype)
						self.process.only_show_sum()
						break

			else:
				Out.error('No option was chosen!')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="Checks and Compare the sums.",
		usage="shazam [OPTION] content..."
	)

	option = parser.add_mutually_exclusive_group()

	option.add_argument("-f", "--file", metavar='', help="Checks the sum of only one file written in the text file.")

	option.add_argument("-F", "--Files", metavar='', help="Checks the sum of all files written  in the text file.")

	option.add_argument("-a", "--all", help="Print all the file's sums.", metavar='')

	option.add_argument("-v", "--version", help="Print the current version of this program.", action="store_true")

	if argv_len == 2:
		option.add_argument("content", help="file name or sum depending of option the choiced", nargs='?')

	for item in Analyze.sumtypes_list:
		option.add_argument("-%s" % item, help="for comparing the file's hash", metavar='', nargs=2)
		option.add_argument("--%ssum" % item, metavar='', help="for just getting the file's hash", nargs='?')

	if argv_len > 1:
		mf = MainFlow(parser.parse_args())
		mf.make_process()

	else:
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
