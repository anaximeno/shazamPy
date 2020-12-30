#!/usr/bin/python3

import os
import sys
import hashlib as hlib

from time import sleep
from alive_progress import alive_bar
from termcolor import colored as clr

# don't ever change this number
BUF_SIZE = 32768

def out_error(err, exit=True):
	print("shazam: error:", err)
	if exit:
		sys.exit(1)


class OutPut:

	def __init__(self, filename, givensum, sumtype):
		self.filename = filename
		self.givensum = givensum
		self.sumtype = sumtype

	def results(self, sucess):
		if sucess:
			print(
				clr(f"# {self.filename}: {self.sumtype}sum is ok!\n", "green")
			)
		else:
			print(
				clr(f"# {self.filename}: {self.sumtype}sum is not the same as the given!\n", "red")
			)

	def verbose(self, hashlist):
		print(
			f" -> Given sum: {self.givensum}\n",
			f"-> '{self.filename}' {self.sumtype}sum: {hashlist[self.sumtype].hexdigest()}"
		)


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
			out_error(f"{filename} is unreadable, must be a file with the sums and filename inside!")
			return False
	else:
		out_error(f"{filename} do not exits in this dir!")

def get_sumtype(filename, hlist):
	if readable(filename):
		# The reverse here is proposal
		for sumtype in list(hlist.keys())[::-1]:
			if sumtype in filename:
				return sumtype

		out_error("Sumtype was not recognized!" )
		return False


class CheckVars():

	def __init__(self, filename, givensum):
		self.filename = filename
		self.givensum = givensum

	# analyze the existence and the sum conditions
	def analyze_content(self):
		if exists(self.filename) and _hex(self.givensum):
			return True
		elif not exists(self.filename):
			out_error("'%s' was not found!" % self.filename)
		elif not _hex(self.givensum):
			out_error("'%s' is not an hexadecimal number!" % self.givensum)

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
								out_error(f"irregularity in the line {l} of '{self.filename}', " +
										"sum must be an hexadecimal value!")
					except ValueError:
						out_error(f"'{self.filename}' must have the file sum and the file name in each"+
								  f"line!\nIrregularity in line {l}.")

					found = ((item, file_base[item], sumtype) for item in file_base if exists(item))
					unfound = (item for item in file_base if not exists(item))

					return found, unfound
			except FileNotFoundError:
				out_error(f"'{self.filename}' was not found!")


def gen_data(f):
	size = os.path.getsize(f)
	i = 0

	if size < BUF_SIZE:
		times = 1
	elif size % BUF_SIZE == 0:
		times = size / BUF_SIZE
	else:
		size -= size % BUF_SIZE
		times = int(size / BUF_SIZE) + 1

	with alive_bar(times, bar='blocks', spinner='dots') as bar:
		with open(f, 'rb') as f:
			while i < times:
				file_data = f.read(BUF_SIZE)	
				yield file_data
				# when lower is the sleep value, faster will be the reading,
				# but it will increase the CPU usage
				sleep(0.00001)
				i += 1
				bar()


class Make:

	def __init__(self, filename, hashlist, givensum=None, sumtype=None):
		self.filename = filename
		self.givensum = givensum
		self.sumtype = sumtype
		self.hlist = hashlist
		self.out = OutPut(filename=filename, sumtype=sumtype, 
						givensum=givensum)

	# read and set the file's sum
	def read(self, sumtype, generated_data):
		for file_data in generated_data:
			self.hlist[sumtype].update(file_data)

	# it checkv if the file's sum is equal to the given sum
	def check(self):
		if int(self.hlist[self.sumtype].hexdigest(), 16) == int(self.givensum, 16):
			self.out.results(True)
		else:
			self.out.results(False)


class Process:

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
		if exists(filename):
			self.make = Make(filename=self.filename, hashlist=self.hlist,
							givensum=self.givensum, sumtype=self.sumtype)
		else:
			out_error(f"'{self.filename}' was not found!")

	# if we have the file's name and sum
	def normal(self):
		if self.checkv.analyze_content():
			
			self.make.read(self.sumtype, gen_data(self.filename))
			self.make.check()

	# TODO: handle when check multifiles's sum, need to eliminate the shadows of the privious check
	def multifiles(self):
		checkv = CheckVars(filename=self.filename, givensum=None)
		found, unfound = checkv.analyze_text(self.hlist)

		for f in found:
			filename, givensum, sumtype = f
			p = Process(filename=filename, givensum=givensum, sumtype=sumtype)
			p.normal()

		print("\nThis/these file(s) wasn't/weren't found:")
		for f in unfound:
			print("* ", f)
		print('\n** If nothing appears, it means all files were found! **')

	# get all sums
	def allsums(self):
		print("Calculating sum...")
		generated_data = list(gen_data(self.filename))
		with alive_bar(len(self.hlist.keys()), spinner='waves') as bar:
			print("Getting hashes...")
			for sumtype in self.hlist.keys():
				self.make.read(sumtype, generated_data)
				bar()

		for sumtype, fsum in self.hlist.items():
			print(f"{sumtype}sum: {fsum.hexdigest()} {self.filename}")

	# if we want only show the sum and no to compare it
	def only_sum(self):
		if exists(self.filename):
			self.make.read(self.sumtype, gen_data(self.filename))

			print(f"\n{self.hlist[self.sumtype].hexdigest()} {self.filename}")
		else:
			out_error(f"'{self.filename}' was not found!")

	def verbose(self):
		op = OutPut(filename=self.filename,
					sumtype=self.sumtype, givensum=self.givensum)
		op.verbose(self.hlist)
