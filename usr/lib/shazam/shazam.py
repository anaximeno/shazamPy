#!/usr/bin/python3

# TODO: must check if the imports of all modules are working well, if not, mssss
import sys
import hashlib as hlib
import argparse

from common import Process, CheckVars, out_error

hlist = {
	"type": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
	"hash": [hlib.md5(), hlib.sha1(), hlib.sha224(), hlib.sha256(), hlib.sha384(), hlib.sha512()],
	"othernames": ["md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum"],
	"pluralnames": ["md5sums", "sha1sums", "sha224sums", "sha256sums", "sha384sums", "sha512sums"]
}

parser = argparse.ArgumentParser(
	description="Check and Compare the sums.",
	usage="shazam [OPTION] content...",
	epilog="Author: Anaxímeno Brito, <anaximenobrito@gmail.com>"
)

option = parser.add_mutually_exclusive_group()

option.add_argument("-f", "--file",
					help="Check the sum of only one file which have the name and sum wrote in the file.")

option.add_argument("-F", "--Files",
					help="Check the sum of all files which have the name and sum wrote in the file.")

option.add_argument("-A", "--all", help="Print all the file's sums.")

option.add_argument(
	"-v", "--version", help="Print the current version of this app.", action="store_true")

option.add_argument(
	"content", help="file name or sum depending of the choice", nargs='?', default=None)

parser.add_argument("--verbose", help="Verbose response", action="store_true")

for item in hlist['type']:
	option.add_argument("-%s" % item, help="to compare the file's hash",
						metavar='', nargs=2)  # metavar is empty
	option.add_argument("--%ssum" % item,
						metavar='', help="to get the file's hash")


# TODO: Ainda falta fazer o processamento na classe para verbose
# TODO: Quando for do tipo ler arquivo de txt e fazer para um só arquivo, 
# precisa tentar todo os nomes dentro e procurar o que funciona, ou fazer isso o processo normal
class MainFlow:

	def __init__(self, args):
		self.args = args

		self.stype = None
		self.fname = None
		self.gsum = None

		simple = {
			"options": [args.md5, args.sha1, args.sha224, args.sha256, args.sha384, args.sha512],
			"sumtype": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],

		}

		only_one = {
			"options": [args.md5sum, args.sha1sum, args.sha224sum, args.sha256sum, args.sha384sum, args.sha512sum],
			"sumtype": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],

		}

		for opt in simple["options"]:
			if opt:
				self.fname, self.gsum = opt
				index = simple["options"].index(opt)
				self.stype = simple["sumtype"][index]

		if not self.fname:
			for opt in only_one["options"]:
				if opt:
					self.fname = opt
					index = only_one["options"].index(opt)
					self.stype = only_one["sumtype"][index]
					self.gsum = None
					
			if not self.fname:
				if args.file:
					checkv = CheckVars(filename=args.file, givensum=None, hashlist=hlist)
					found, unfounded = checkv.analyze_text()
					if found:
						self.fname, self.gsum, self.stype = found[0]
					else:
						out_error("None of these file(s) was/were found:", exit=False)
						for unf in unfounded:
							print("*", unf)
						sys.exit(1)

				elif args.Files:
					self.fname = args.Files

				elif args.all:
					self.fname = args.all

				elif args.content:
					self.fname = args.content

		self.process = Process(filename=self.fname, sumtype=self.stype, givensum=self.gsum)
		
	def make_process(self):
		if (self.fname and self.stype and self.gsum) or self.args.file:
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

if __name__ == '__main__':
	if len(sys.argv) > 1:
		mf = MainFlow(parser.parse_args())
		mf.make_process()
	else:
		print("Usage: shazam [Option] ARGUMENTS..")
		print("       shazam --help	        display the help section and exit")
		print("       shazam --version      display the Version information and exit")
