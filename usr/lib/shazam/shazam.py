#!/usr/bin/python3

# TODO: must check if the imports of all modules are working well, if not, mssss
import sys
import hashlib as hlib
import argparse

from common import Process, CheckVars, out_error, _hex

hlist = {
	"md5": hlib.md5(),
	"sha1": hlib.sha1(),
	"sha224": hlib.sha224(),
	"sha256": hlib.sha256(),
	"sha384": hlib.sha384(),
	"sha512": hlib.sha512()
}

parser = argparse.ArgumentParser(
	description="Check and Compare the sums.",
	usage="shazam [OPTION] content..."
)

option = parser.add_mutually_exclusive_group()

option.add_argument("-f", "--file", metavar='',
					help="Check the sum of only one file which have the name and sum wrote in the file.")

option.add_argument("-F", "--Files", metavar='',
					help="Check the sum of all files which have the name and sum wrote in the file.")

option.add_argument("-a", "--all", help="Print all the file's sums.", metavar='')

option.add_argument(
	"-v", "--version", help="Print the current version of this app.", action="store_true")

option.add_argument(
	"content", help="file name or sum depending of the choice", nargs='?', default=None)

parser.add_argument("--verbose", help="Verbose response", action="store_true")

for item in hlist.keys():
	option.add_argument("-%s" % item, help="to compare the file's hash",
						metavar='', nargs=2)  # metavar is empty
	option.add_argument("--%ssum" % item,
						metavar='', help="to get the file's hash")


# TODO: Ainda falta fazer o processo para verbose
class MainFlow:

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
				out_error("This/these file(s) wasn't/weren't found:", exit=False)
				for f in unfound:
					print("*", f)
				sys.exit(1)

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
					if not _hex(opt[0][0]):	
						self.fname, self.gsum = opt[0]
					else:
						self.gsum, self.fname = opt[0]			
					self.stype = stype
					break
				elif opt[1]:
					self.fname = opt[1]
					self.stype = stype
					self.gsum = None
					break

		self.process = Process(filename=self.fname, sumtype=self.stype, givensum=self.gsum)
		
	def make_process(self):
		if self.fname and self.stype and self.gsum or self.args.file:
			self.process.normal()
		elif self.fname and self.stype:
			self.process.only_sum()
		elif self.args.Files:
			self.process.multifiles()
		elif self.args.all or self.args.content:
			self.process.allsums()
		elif self.args.version:
			with open("/usr/share/shazam/VERSION", "rt") as ver:
				print( "ShaZam", str(ver.read()) )
		else:
			out_error("Anything went wrong")


if __name__ == '__main__':
	if len(sys.argv) > 1:
		mf = MainFlow(parser.parse_args())
		mf.make_process()
	else:
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help         display the help section and exit")
		print("       shazam --version      display the Version information and exit")
