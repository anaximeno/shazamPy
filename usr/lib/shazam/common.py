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



import os
import sys
import hashlib as hlib
from time import sleep

try :
	from termcolor import colored as clr
	from alive_progress import alive_bar

except ImportError :
	sys.exit("Important Modules are not installed yet: termcolor, " +
	"alive_progress.\nInstall them with: pip (or pip3) install termcolor " +
	"alive_progress")



class Out :
	def __init__(self, filename, sumtype) :
		self.fname, self.stype = filename, sumtype
		
	@staticmethod
	def error(*err, exit=True) :
		"""print error message and exit"""
		error_message = ' '.join(err)
		print("ShaZam: ERROR: %s" % error_message)
		
		if exit :
			sys.exit(1)

	def results(self, success) :
		"""print result depending of the success attribute"""
		if success :
			print(clr(f"# {self.fname}: {self.stype}sum is ok!\n", "green"))
		
		else :
			print(clr(f"# {self.fname}: {self.stype}sum is not the same as the given!\n", "red"))


class Analyze :
	sumtypes_list = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

	@staticmethod
	def is_hex(hexa) :
		"""Checks if is hexadecimal and return bool"""
		try :
			int(hexa, 16)
			return True

		except ValueError :
			return False

	@staticmethod
	def exists(filename) :
		"""Searchs for a file and return bool"""
		current_folder = os.listdir()

		if filename in current_folder:
			return True

		else :
			try:
				with open(filename, 'rb') as target:
					if target:
						return True

			except IOError :
				return False

	@classmethod
	def readable(cls, filename) :
		"""Analyses de readability and return bool"""
		if cls.exists(filename) :
			try:
				with open(filename, "rt") as f :
					f.read(1)
					return True

			except UnicodeDecodeError :
				Out.error(f"File is unreadable: {filename!r}")
				return False

		else :
			Out.error(f"File not found: {filename!r}")

	@classmethod
	def sumtype(cls, filename):
		"""Get file and return sumtype"""
		if cls.readable(filename):
			for stype in cls.sumtypes_list[::-1]:
				if stype in filename:
					return stype
		
			Out.error(f"Sumtype not recognized in: {filename}")

	@classmethod
	def contents(cls, filename) :
		"""Return the content of the file"""
		if cls.exists(filename) is True :
			content = {}
		
			with open(filename, "rt") as t :
				try:
					for line in t :
						gsum, fname = line.split()
		
						if fname[0] == '*' and not cls.exists(fname[0]) :
							fname = fname[1:]
		
						content[fname] = gsum
		
				except ValueError :
					Out.error(f"Reading error: must have the sum of the file and the file name respectively on each line.")
		
				return content
		
		else :
			Out.error(f"File not found: {filename!r}")


class Make :
	BUF_SIZE = 32768

	def __init__(self, filename, hashlist) :
		self.filename = filename
		self.hlist = hashlist

	def gen_data(self, bars=True) :
		"""Generates binary data"""
		size = os.path.getsize(self.filename)

		if size < self.BUF_SIZE :
			times = 1
		
		elif size % self.BUF_SIZE == 0 :
			times = int(size / self.BUF_SIZE)
		
		else :
			size -= size % self.BUF_SIZE
			times = int(size / self.BUF_SIZE) + 1

		def generate_data(f) :
			file_data = f.read(self.BUF_SIZE)
			yield file_data
			# when lower is the sleep value, faster will be the reading,
			# but it will increase the CPU usage
			sleep(0.00001)

		if bars :
			with alive_bar(times, bar='blocks', spinner='dots') as bar :
				with open(self.filename, 'rb') as f:
					for _ in range(times) :
						yield from generate_data(f)
						bar()
		
		else:
			with open(self.filename, 'rb') as f :
				for _ in range(times) :
					yield from generate_data(f)

	def update(self, sumtype, generated_data) :
		"""Updates binary data for hexdigest"""
		for file_data in generated_data :
			self.hlist[sumtype].update(file_data)
		
		else :
			return True

	# it checkv if the file's sum is equal to the given sum
	def check(self, sumtype, givensum) :
		"""Compares file's sum with givensum"""
		out = Out(self.filename, sumtype)
		if int(self.hlist[sumtype].hexdigest(), 16) == int(givensum, 16) :
			out.results(True)
			return True
		
		else :
			out.results(False)
			return False


class FileId(object) :
	"""Holds all file's informations"""
	def __init__(self, name, givensum=None) :
		self.name = name
		self.existence = Analyze.exists(name)

		if self.existence is True:
			self.hlist = {
				"md5": hlib.md5(),
				"sha1": hlib.sha1(),
				"sha224": hlib.sha224(),
				"sha256": hlib.sha256(),
				"sha384": hlib.sha384(),
				"sha512": hlib.sha512()
			}

		if givensum :
			self.gsum = givensum
			self.valid_gsum = Analyze.is_hex(givensum)
			
	def __str__(self) :
		return str(self.name)

	def get_hash_sum(self, sumtype) :
		"""Return the file's hash sum"""
		if self.existence is True :
			return self.hlist[sumtype].hexdigest()
		
		Out.error(f"File not found: {self.name!r}\nCan't Give hash sum")


class Process :

	def __init__(self, sumtype=None, *files) :

		try :
			self.files = list(files)
		
		except TypeError :
			self.files = []

		self.sumtype = sumtype

	def add_file(self, filename) :
		self.files.append(filename)

	def define_sumtype(self, sumtype) :
		self.sumtype = sumtype

	def check_process(self) :
		"""Check and Compare the hash sums of one file."""
		fileid = self.files[0]
		
		if fileid.existence is False :
			Out.error(f"File not found: {fileid.name!r}")
		
		elif fileid.valid_gsum is False :
			Out.error(f"Given sum is not Hexadecimal: {fileid.gsum!r}")
		
		elif not self.sumtype :
			Out.error("Sumtype is Undefined")
		
		else :
			make = Make(filename=fileid.name, hashlist=fileid.hlist)
			make.update(self.sumtype, make.gen_data())
			make.check(self.sumtype, fileid.gsum)

	def only_show_sum(self) :
		"""Only calculates and print the file's hash sum."""
		if not self.sumtype :
			Out.error("Sumtype is Undefined")
		
		elif len(self.files) > 1 :
			found = [f for f in self.files if f.existence is True]
			unfound = [f.name for f in self.files if f not in found]

			with alive_bar(len(found), bar='blocks', spinner='dots') as bar :
				for fileid in found :
					make = Make(filename=fileid.name, hashlist=fileid.hlist)
					make.update(self.sumtype, make.gen_data(bars=False))
					print(f"{fileid.get_hash_sum(self.sumtype)} {fileid.name}")
					bar()

			print("\nThis/these file(s) wasn't/weren't found:")
			for filename in unfound :
				print("* ", filename)
			print('\n ** If nothing appears above, it means that all files have been found **')

		elif len(self.files) == 1 :
			fileid = self.files[0]
			
			if fileid.existence is True :
				make = Make(filename=fileid.name, hashlist=fileid.hlist)
				make.update(self.sumtype, make.gen_data())
				print(f"\n{fileid.get_hash_sum(self.sumtype)} {fileid.name}\n")
			
			else :
				Out.error(f"File not found: {fileid.name!r}")
		
		else :
			Out.error("File was not given!")
			
	def check_multifiles(self) :
		"""Checks and compare the hash sums of more than one files."""
		found = [f for f in self.files if f.existence is True]
		unfound = [f.name for f in self.files if f not in found]

		with alive_bar(len(found), bar='blocks', spinner='dots') as bar :
			for fileid in found :
				if fileid.valid_gsum is False :
					Out.error(f"Given sum is not Hexadecimal: {fileid.gsum!r}")
		
				elif not self.sumtype :
					Out.error("Sumtype is Undefined")
		
				else :
					make = Make(filename=fileid.name, hashlist=fileid.hlist)
					make.update(self.sumtype, make.gen_data(bars=False))
					make.check(self.sumtype, fileid.gsum)
					bar()
		
		print("\nThis/these file(s) wasn't/weren't found:")
		for filename in unfound :
			print("* ", filename)
		print('\n ** If nothing appears above, it means that all files have been found **')

	def show_allsums(self) :
		"""Print all supported hash sums of one file."""
		fileid = self.files[0]
		
		if fileid.existence is True :
			make = Make(filename=fileid.name, hashlist=fileid.hlist)
			print("Calculating sum...")
			generated_data = list(make.gen_data())
		
			with alive_bar(len(fileid.hlist.keys()), spinner='waves') as bar :
				print("Getting hashes...")
				for sumtype in fileid.hlist.keys() :
					make.update(sumtype, generated_data)
					# when lower is the sleep value, faster will be the reading,
					# but it will increase the CPU usage
					sleep(0.00001)
					bar()

			for sumtype in fileid.hlist.keys() :
				print(f"{sumtype}sum: {fileid.get_hash_sum(sumtype)} {fileid.name}")
		
		else :
			Out.error(f"File not found: {fileid.name!r}")
