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

	def __init__(self, filename=None, givensum=None, sumtype=None):
		self.fname = filename
		self.gsum = givensum
		self.stype = sumtype

	def results(self, sucess):
		if sucess:
			print(
				clr(" '%s' %ssum matched perfectly!" %
					(self.fname, self.stype), "green")
			)
		else:
			print(
				clr(" '%s' %ssum did not match!" %
					(self.fname, self.stype), "red")
			)

	def verbose(self, hashlist):
		index = hashlist['type'].index(self.stype)
		filesum = hashlist['hash'][index].hexdigest()

		print(
			" -> Given sum: %s\n" % self.gsum,
			"-> '%s' %ssum: %s" % (self.fname, self.stype, filesum),
		)


# check the existence of the file
def exists(fname):
	try:
		with open(fname, 'rb') as target:
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


def is_readable(fname):
	if exists(fname):
		try:
			with open(fname, "rt") as f:
				f.read(1)
				return True
		except UnicodeDecodeError:
			out_error(
				"%s is unreadable, must be a file with the sums and filename inside!" % fname)
			return False
	else:
		out_error("%s do not exits in this dir!" % fname)


class Validate:

	def __init__(self, filename, hashlist):
		self.fname = filename
		self.hlist = hashlist

	def sumtype(self):
		if is_readable(self.fname):
			text_path = self.fname.split('/')
			otxt = text_path[-1]
			name = os.path.splitext(otxt)[0]
			if name in self.hlist["type"]:
				return name
			elif name in self.hlist["pluralnames"]:
				index = self.hlist["pluralnames"].index(name)
				return self.hlist["type"][index]
			elif name in self.hlist["othernames"]:
				index = self.hlist["othernames"].index(name)
				return self.hlist["type"][index]
			else:
				out_error(
					"'%s' was not recognized as a supported sum type!" % name)
				return False


class CheckVars:

	def __init__(self, filename, givensum, hashlist):
		self.fname = filename
		self.gsum = givensum
		self.validate = Validate(self.fname, hashlist)

	# analyze the existence and the sum conditions
	def analyze_file(self):
		if exists(self.fname) and _hex(self.gsum):
			return True
		elif not exists(self.fname):
			out_error("'%s' was not found!" %
					self.fname)
		elif not _hex(self.gsum):
			out_error("'%s' is not an hexadecimal number!" % self.gsum)

	# analyze the content of the sum.txt given
	def analyze_text(self):
		if self.validate.sumtype():
			try:
				file_base = {}
				with open(self.fname, "rt") as t:
					try:
						l = 0
						for line in t:
							l += 1
							givensum, filename = line.split()
							if _hex(givensum):
								file_base[filename] = givensum
							else:
								out_error("irregularity in the line %s of '%s', " % l % self.fname +
										"sum must be an hexadecimal value!")
					except ValueError:
						out_error("'%s' must have the file sum and the file name in each" % self.fname +
								"line!\nIrregularity in line %s." % l)

					unfounded = []
					found = []

					def find(filename):
						if exists(filename):
							found.append(
								(filename, file_base[filename], self.validate.sumtype()))
						else:
							unfounded.append(filename)

					for item in file_base:
						find(item)

					return found, unfounded
			except FileNotFoundError:
				out_error("'%s' was not found!" % self.fname)


# this is used below to gen data
def gen(dt):
	if dt:
		yield dt


class Make:

	def __init__(self, filename, hashlist, givensum=None, sumtype=None):
		self.fname = filename
		self.gsum = givensum
		self.stype = sumtype
		self.hlist = hashlist
		self.out = OutPut(filename=self.fname, sumtype=self.stype, 
						givensum=self.gsum)

	# read all sums
	def all_sums(self):
		with alive_bar(len(self.hlist['type']), bar='blocks', spinner='dots') as bar:
			for item in self.hlist['type']:
				with open(self.fname, 'rb') as f:
					while True:
						try:
							file_data = gen(f.read(BUF_SIZE))
							index = self.hlist['type'].index(item)
							filesum = self.hlist['hash'][index]
							filesum.update(next(file_data))
							# when lower is the sleep value, faster will be the reading,
							# but it will increase the CPU usage
							sleep(0.00001)
						except StopIteration:
							break
				bar()

	# read and set the file's sum
	def read(self):
		size = os.path.getsize(self.fname)
		times = 0

		while size > 0:
			size -= BUF_SIZE
			times += 1

		with alive_bar(times, bar='filling', spinner='dots') as bar:
			with open(self.fname, 'rb') as f:
				while True:
					try:
						file_data = gen(f.read(BUF_SIZE))
						index = self.hlist['type'].index(self.stype)
						filesum = self.hlist['hash'][index]
						filesum.update(next(file_data))
						# when lower is the sleep value, faster will be the reading,
						# but it will increase the CPU usage
						sleep(0.00001)
						bar()
					except StopIteration:
						break

	# it checks if the file's sum is equal to the given sum
	def check(self):
		index = self.hlist['type'].index(self.stype)
		filesum = self.hlist['hash'][index].hexdigest()

		if int(filesum, 16) == int(self.gsum, 16):
			self.out.results(True)
		else:
			self.out.results(False)


class Process:

	def __init__(self, filename, sumtype=None, givensum=None):
		self.stype = sumtype
		self.gsum = givensum
		self.fname = filename

		self.hlist = {
			"type": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
			"hash": [hlib.md5(), hlib.sha1(), hlib.sha224(), hlib.sha256(), hlib.sha384(), hlib.sha512()],
			"othernames": ["md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum"],
			"pluralnames": ["md5sums", "sha1sums", "sha224sums", "sha256sums", "sha384sums", "sha512sums"]
		}

		self.checks = CheckVars(filename=self.fname, givensum=self.gsum, hashlist=self.hlist)
		self.make = Make(filename=self.fname, hashlist=self.hlist,
						givensum=self.gsum, sumtype=self.stype)

	# if we have the file's name and sum
	def normal(self):
		if self.checks.analyze_file():
			self.make.read()
			self.make.check()

	# TODO: handle when check multifiles's sum, need to eliminate the shadows of the privious check
	def multifiles(self):
		checks = CheckVars(filename=self.fname, givensum=None, hashlist=self.hlist)
		found, unfounded = checks.analyze_text()
		if found:
			for ifound in found:
				fname, gsum, stype = ifound
				procs = Process(filename=fname, givensum=gsum, sumtype=stype)

				procs.normal()

				if unfounded:
					print("The file(s) below was/were not found:")
					for unf in unfounded:
						print("* ", unf)
		else:
			print("None of the file(s) below was/were found:")
			for unf in unfounded:
				print("* ", unf)

	# get all sums
	def allsums(self):
		if exists(self.fname):
			self.make.all_sums()
			print("\nAll '%s' sums below: " % self.fname)
			for item in self.hlist['type']:
				index = self.hlist['type'].index(item)
				filesum = self.hlist['hash'][index].hexdigest()
				print(" -> %ssum: %s" % (item, filesum))
		else:
			out_error("'%s' was not found!" % self.fname)

	# if we want only show the sum and no to compare it
	def only_sum(self):
		if exists(self.fname):
			self.make.read()
			index = self.hlist['type'].index(self.stype)
			filesum = self.hlist['hash'][index].hexdigest()
			print("'%s' %ssum is: %s" % (self.fname, self.stype, filesum))
		else:
			out_error("'%s' was not found!" % self.fname)

	def verbose(self):
		op = OutPut(filename=self.fname,
					sumtype=self.stype, givensum=self.gsum)
		op.verbose(self.hlist)
