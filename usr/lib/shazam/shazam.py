#!/usr/bin/python3
import sys
import hashlib as hlib
from time import sleep

from common import Process, CheckVars, out_error, _hex, results

try:
	import argparse
	from alive_progress import alive_bar
except ImportError:
	out_error("Important Modules are not installed yet: argparse, alive_progress\n\
		Install them with: pip/pip3 install argparse alive_progress")

hlist = {
	"md5": hlib.md5(),
	"sha1": hlib.sha1(),
	"sha224": hlib.sha224(),
	"sha256": hlib.sha256(),
	"sha384": hlib.sha384(),
	"sha512": hlib.sha512()
}


# TODO: Ainda falta fazer o processo para verbose
class MainFlow(object):

	def __init__(self, args):
		self.args = args

		self.stype = None
		self.fname = None
		self.gsum = None

		options = {
			'md5': (args.md5, args.md5sum),
			'sha1': (args.sha1, args.sha1sum),
			'sha224': (args.sha224, args.sha224sum),
			'sha256': (args.sha256, args.sha256sum),
			'sha384': (args.sha384, args.sha384sum),
			'sha512': (args.sha512, args.sha512sum)
		}

		if args.file:
			checkv = CheckVars(filename=args.file, givensum=None)
			found, unfound = checkv.analyze_text(hlist)

			found = list(found)

			if found:
				self.fname, self.gsum, self.stype = found[0]
			else:
				print("This/these file(s) wasn't/weren't found:")
				for f in unfound:
					print("* ", f)
				sys.exit(0)

		elif args.Files:
			self.fname = args.Files

		elif args.all:
			self.fname = args.all

		elif args.content:
			self.fname = args.content

		else:
			for stype, opt in options.items():
				if opt[0]:
					# TODO: pass the expression below to a function, to be used when reading txt files
					if _hex(opt[0][1]):
						self.fname, self.gsum = opt[0]
					elif _hex(opt[0][0]):
						self.gsum, self.fname = opt[0]			
					else:
						out_error(f"File sum not hexadecimal value: '{opt[0][0]} {opt[0][1]}'")
					self.stype = stype
					break
				elif opt[1]:
					self.fname = opt[1]
					self.stype = stype
					self.gsum = None
					break
		
		if self.fname:
			self.process = Process(filename=self.fname, sumtype=self.stype, givensum=self.gsum)
		
	def make_process(self):  # TODO: args.file: must find search for all the files until find one Sucess case
		if self.fname and self.stype and self.gsum or self.args.file:
			self.process.make_and_check()

		elif self.fname and self.stype:
			self.process.only_show_sum()

		elif self.args.Files:
			checkv = CheckVars(self.fname, givensum=None)
			found, unfound = checkv.analyze_text(hlist)

			def check_multifiles(filename, givensum, sumtype):
				p = Process(
					filename=filename,
					sumtype=sumtype,
					givensum=givensum,
				)

				p.make.read(sumtype, p.make.gen_data(bars=False))
				if int(p.hlist[sumtype].hexdigest(), 16) == int(givensum, 16):
					return True
				else:
					return False

			nfound = list(found)
			if nfound:
				with alive_bar(len(nfound), bar='blocks', spinner='dots') as bar:
					for fname, gsum, stype in nfound:
						results(fname, stype, check_multifiles(fname, gsum, stype))
						# when lower is the sleep value, faster will be the reading,
						# but it will increase the CPU usage
						sleep(0.00001)
						bar()

			print("\nThis/these file(s) wasn't/weren't found:")
			for f in unfound:
				print("* ", f)
			print('\n ** If nothing appears above, it means that all files have been found **')

		elif self.args.all or self.args.content:
			self.process.show_allsums()

		elif self.args.version:
			with open("/usr/share/shazam/VERSION", "rt") as ver:
				print("ShaZam", str(ver.read()).strip())

		else:
			out_error("Anything went wrong")


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

	option.add_argument("content", help="file name or sum depending of the choice", nargs='?', default=None)

	# parser.add_argument("--verbose", help="Verbose response", action="store_true")

	for item in hlist.keys():
		option.add_argument("-%s" % item, help="for comparing the file's hash", metavar='', nargs=2)
		option.add_argument("--%ssum" % item, metavar='', help="for just getting the file's hash")

	if len(sys.argv) > 1:
		mf = MainFlow(parser.parse_args())
		mf.make_process()
	else:
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
