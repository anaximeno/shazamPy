#!/usr/bin/python3
import os
import sys
import hashlib as hlib

from time import sleep
from alive_progress import alive_bar


def out_error(err, exit=True):
	if exit:
		sys.exit("ShaZam: ERROR: %s" % err)
	else:
		print("ShaZam: ERROR: %s" % err)


try:
	from termcolor import colored as clr
except ImportError:
	out_error("Important Module is not installed yet: alive_progress, termcolor\n\
		Install it with: pip/pip3 termcolor")

# don't ever change this number
BUF_SIZE = 32768


def results(filename, sumtype, sucess):
	if sucess:
		print(clr(f"# {filename}: {sumtype}sum is ok!\n", "green"))
	else:
		print(clr(f"# {filename}: {sumtype}sum is not the same as the given!\n", "red"))


# check the existence of the file
def exists(filename):
	folder = os.listdir()
	if filename in folder:
		return True
	else:
		try:
			with open(filename, 'rb') as target:
				if target:
					return True
		except IOError:
			return False


# check if the value is an hexadecimal value
def _hex(hexa):
	try:
		int(hexa, 16)
		return True
	except ValueError:
		return False


def readable(filename):
	if exists(filename):
		try:
			with open(filename, "rt") as f:
				f.read(1)
				return True
		except UnicodeDecodeError:
			out_error(f"File is unreadable: {filename!r}")
			return False
	else:
		out_error(f"File not found: {filename!r}")


def get_sumtype(filename, hlist):
	if readable(filename):
		# The reverse below is proposal
		for sumtype in list(hlist.keys())[::-1]:
			if sumtype in filename:
				return sumtype

		out_error("Sumtype was not recognized: {filename}")
		return False


class CheckVars(object):
	__slots__ = ['filename', 'givensum']

	def __init__(self, filename, givensum):
		self.filename = filename
		self.givensum = givensum

	# analyze the existence and the sum conditions
	def analyze_content(self):
		if exists(self.filename) and _hex(self.givensum):
			return True
		elif not exists(self.filename):
			out_error(f"File not found: {self.filename!r}")
		elif not _hex(self.givensum):
			out_error(f"File sum not hexadecimal value: {self.givensum}")

	# analyze the content of the sum.txt given
	def analyze_text(self, hashlist):
		sumtype = get_sumtype(self.filename, hashlist)
		if sumtype:
			try:
				file_base = {}
				with open(self.filename, "rt") as t:
					try:
						l = 0
						for line in t:
							l += 1
							givensum, filename = line.split()

							if '*' == filename[0] and not exists(filename[0]):
								filename = filename[1:]
							else:
								pass
							# TODO: must check if the first part is hex and the second part exists or vice
							if _hex(givensum):
								file_base[filename] = givensum
							else:
								out_error(f"File sum not hexadecimal value: irregularity in the line {l}")
					except ValueError:
						out_error(f"Read error: must have the sum of the file and the file name respectively on each line\n\
						Irregularity in line {l}.")

					found = ((item, file_base[item], sumtype) for item in file_base if exists(item))
					unfound = (item for item in file_base if not exists(item))

					return found, unfound
			except FileNotFoundError:
				out_error(f"File not found: {self.filename!r}")


class Make(object):

	def __init__(self, filename, hashlist, givensum=None, sumtype=None):
		self.filename = filename
		self.givensum = givensum
		self.sumtype = sumtype
		self.hlist = hashlist

	def gen_data(self, bars=True):
		size = os.path.getsize(self.filename)

		if size < BUF_SIZE:
			times = 1
		elif size % BUF_SIZE == 0:
			times = size / BUF_SIZE
		else:
			size -= size % BUF_SIZE
			times = int(size / BUF_SIZE) + 1

		def generate_data(f):
			file_data = f.read(BUF_SIZE)
			yield file_data
			# when lower is the sleep value, faster will be the reading,
			# but it will increase the CPU usage
			sleep(0.00001)

		if bars:
			with alive_bar(times, bar='blocks', spinner='dots') as bar:
				with open(self.filename, 'rb') as f:
					for _ in range(times):
						yield from generate_data(f)
						bar()
		else:
			with open(self.filename, 'rb') as f:
				for _ in range(times):
					yield from generate_data(f)

	# read and set the file's sum
	def read(self, sumtype, generated_data):
		for file_data in generated_data:
			self.hlist[sumtype].update(file_data)

	# it checkv if the file's sum is equal to the given sum
	def check(self):
		if int(self.hlist[self.sumtype].hexdigest(), 16) == int(self.givensum, 16):
			results(self.filename, self.sumtype, True)
		else:
			results(self.filename, self.sumtype, False)


class Process(object):
	def __init__(self, filename, sumtype=None, givensum=None):
		self.sumtype = sumtype
		self.givensum = givensum
		self.filename = filename

		self.hlist = {
			"md5": hlib.md5(),
			"sha1": hlib.sha1(),
			"sha224": hlib.sha224(),
			"sha256": hlib.sha256(),
			"sha384": hlib.sha384(),
			"sha512": hlib.sha512()
		}

		self.checkv = CheckVars(filename=self.filename, givensum=self.givensum)

		if self.filename:
			self.make = Make(filename=self.filename, hashlist=self.hlist, givensum=self.givensum, sumtype=self.sumtype)

	# if we have the file's name and sum
	def make_and_check(self):
		if self.checkv.analyze_content():
			self.make.read(self.sumtype, self.make.gen_data())
			self.make.check()

	# get all sums
	def show_allsums(self):
		if exists(self.filename):
			print("Calculating sum...")
			generated_data = list(self.make.gen_data())
			with alive_bar(len(self.hlist.keys()), spinner='waves') as bar:
				print("Getting hashes...")
				for sumtype in self.hlist.keys():
					self.make.read(sumtype, generated_data)
					# when lower is the sleep value, faster will be the reading,
					# but it will increase the CPU usage
					sleep(0.00001)
					bar()

			for sumtype, fsum in self.hlist.items():
				print(f"{sumtype}sum: {fsum.hexdigest()} {self.filename}")
		else:
			out_error(f"File not found: {self.filename!r}")

	# if we want only show the sum and no to compare it
	def only_show_sum(self):
		if exists(self.filename):
			self.make.read(self.sumtype, self.make.gen_data())

			print(f"\n{self.hlist[self.sumtype].hexdigest()} {self.filename}")
		else:
			out_error(f"File not found: {self.filename!r}")
