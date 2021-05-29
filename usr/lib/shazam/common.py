#!/usr/bin/env python3
""" Common is a support module, which contains the principals methods
and/or functions of this programm."""
# -*- coding: utf-8 -*-

import os
import sys
import hashlib as hlib
from time import sleep
from typing import Generator


def exists(path):
	"""Searchs for a file/path and return bool."""
	return os.path.exists(path)


def print_error(*err: str, exit: bool = True, err_num: int = 1):
	"""Print the error message and exit.\n
	Keyword args: 
		exit --> if is to exit after showing the error (default: True),
		err_num --> number of the error (default: 1)."""
	error_message = ' '.join(err)
	print("Shazam: Error: %s" % error_message)
	if exit: 
		sys.exit(err_num)


to_install = []

# Third-part libraries
try:
	import termcolor.colored as clr
except ImportError:
	to_install.append('termcolor')

try:
	from alive_progress import alive_bar
except ImportError:
	to_install.append('alive_progress')

finally:
	if any(to_install):
		modules_to_install = ', '.join(to_install)
		print_error(f"Must install some modules first: {modules_to_install}!",
		"\nInstall them with pip or conda.")
	else:
		del to_install


__author__ = "Anaxímeno Brito"
__version__ = '0.4.4'
__license__ = "GNU General Public License v3.0"
__copyright__ = "Copyright (c) 2020-2021 by " + __author__


# List of all supported hash sums:
sumtypes_list = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

# BUF_SIZE is Constant, don't change it!
BUF_SIZE = 32768

# When lower is the sleep value, faster will be the reading,
# but it will increase the CPU usage, it can be changed to
# improve the performance.
SLEEP_VALUE = 0.00001


def hexa_to_int(hexa: str):
	"""Receive hexadecimal string and return integer."""
	try : 
		return int(hexa, 16)
	except ValueError:
		print_error(f"{hexa!r} is not an hexadecimal value!")


def readable(fname: str) -> bool:
	"""Analyses de readability and return bool."""
	if os.path.isdir(fname) or not exists(fname):
		return False
	else:
		try:
			# Try to read, at least, one byte of the file to
			# check if it is readable.
			with open(fname, "rb") as f:
				f.read(1)
			return True
		except UnicodeDecodeError:
			return False


def get_sumtype(fname: str):
	"""Analyses the filename and return the sumtype."""
	for stype in sumtypes_list[::-1]:
		if stype in fname: 
			return stype
	return False


def contents(txtfile: str):
	"""Return a `list with tuples` with the content of the file,
	each tuple has the following structure: `(filesum, filename)`."""
	if readable(txtfile):
		try:
			with open(txtfile, "rt") as txt:
				content = [(line.split()[0], line.split()[1]) for line in txt]
			if content:
				return content
			print_error(f"Reading Error: {txtfile!r} is empty!")
		except IndexError:
			print_error(f"Reading Error: Error while reading {txtfile!r}, expected filesum and filename in each line!")
		except UnicodeDecodeError:
			print_error(f"Reading Error: {txtfile!r} is not readable!")
	else:
		prob = 'was not found!' if not exists(txtfile) else 'is not readable!'
		print_error(f"Reading Error: {txtfile!r} {prob}")


def salutations(string: str, sleep_time: float = 0.1):
	lines = string.splitlines()
	for line in lines:
		lag = '\r'
		for char in line:
			lag += char
			sys.stdout.write(lag)
			sys.stdout.flush()
			sleep(sleep_time)
		print('')


class FileID(object):
	"""This class holds all necessary informations and operations
	for one file object."""
	def __init__(self, name, givensum=None):
		# Eliminates asteriscs if there exists one at the beginning
		# of the file name.
		self.name = name if name[0] != '*' or exists(name) else name[1:]
		
		# Directory of the file and splited name
		path = os.path.split(name)
		self.dir, self.only_name = path if path[0] else ('.', path[-1])

		self.existence = exists(name)
		self.readability = readable(name)

		# ´givensum´ is the original file sum which is give at the download place.
		self.gsum = givensum

		# ´self.integer_sum´ is the integer value of the hash sum,
		# it will be used in comparisons for checking if the values are equal.
		self.integer_sum = hexa_to_int(givensum) if givensum else None

		# This list will store all hash types that were calculated.
		self.calculated_sums = []

		if readable(name):
			self.size = os.path.getsize(name)
			# self.hlist dict stores hashlib methods for calculating the hash sums.
			self.hlist = {
				"md5": hlib.md5(),
				"sha1": hlib.sha1(),
				"sha224": hlib.sha224(),
				"sha256": hlib.sha256(),
				"sha384": hlib.sha384(),
				"sha512": hlib.sha512()
			}

	def __str__(self):
		return self.name

	def get_hashsum(self, sumtype: str):
		"""Return the file's hash sum."""
		if sumtype in self.calculated_sums:
			return self.hlist[sumtype].hexdigest()
		print_error(f"{sumtype!r} was not calculated already!")

	def gen_data(self, *, bars: bool = True):
		"""Generates binary data. 
		Keyword arg: 
			bars --> bool (default: True).
		"""
		if self.readability:
			times = (self.size // BUF_SIZE) + (self.size % BUF_SIZE)
			if bars:
				print("        * Calculating Binaries *")
				with alive_bar(times, bar='blocks', spinner='dots') as bar:
					with open(self.name, 'rb') as f:
						for _ in range(times):
							yield f.read(BUF_SIZE)
							sleep(SLEEP_VALUE)
							bar()
			else:
				with open(self.name, 'rb') as f:
					for _ in range(times):
						yield f.read(BUF_SIZE)
						sleep(SLEEP_VALUE)
		else:
			print_error(f"Reading Error: {self.name!r} is not readable!")

	def update_data(self, sumtype: str, generated_data: Generator):
		"""Updates binary data to the sumtype's class."""
		for file_data in generated_data:
			self.hlist[sumtype].update(file_data)
		self.calculated_sums.append(sumtype)

	def checksum(self, sumtype: str):
		"""Compares file's sum with givensum and return the results"""
		if hexa_to_int(self.get_hashsum(sumtype)) == self.integer_sum:
			return clr(f"{self.name}", "green")
		else:
			return clr(f"{self.name} X", "red")


class Process(object):

	def __init__(self, files: list, sumtype: str = None):
		# define the sumtype to be worked with
		self.sumtype = sumtype
		# ´self.found´ and ´self.unfound´ store files depending on their
		# existence/readability or not, and below them are their respective lengths.
		self.found = [f for f in files if f.readability is True]
		self.unfound = [f for f in files if f not in self.found]
		self.n_found = len(self.found)
		self.n_unfound = len(self.unfound)

	def checkfile(self, *, fid: FileID = None, fdata: list = None, bars: bool = True, verbosity: bool = True):
		"""Check and Compare the hash sum."""
		if not self.sumtype:
			print_error("Sumtype was not defined!")
		elif not self.found and self.unfound:
			print_error(f"FileNotFound Error: {self.unfound[0]!r} was not found!")
		elif not self.found and not self.unfound:
			print_error("Files were not given!!")
		else:
			fileid = fid or self.found[0]
			fileid.update_data(
				sumtype=self.sumtype,
				generated_data=fdata or fileid.gen_data(bars=bars)
			)
			print("\n-----", fileid.checksum(self.sumtype))
			if verbosity:
				print(f"|  Original  Hash Sum:  {fileid.gsum!r}")
				print(f"| Calculated Hash Sum:  {fileid.get_hashsum(self.sumtype)!r}")
				print("------------------")

	def calculate_sum(self, verbosity=True):
		"""Calculates and prints the file's hash sum"""
		if not self.sumtype:
			print_error("Sumtype was not defined!")
		elif self.found:
			print("        * Calculating Hashes *")
			with alive_bar(self.n_found, bar='blocks', spinner='dots') as bar:
				for fileid in self.found:
					fileid.update_data(self.sumtype, fileid.gen_data(bars=False))
					if verbosity:
						print(f"{fileid.get_hashsum(self.sumtype)} {fileid.name}")
					bar()

		self.print_unfound()

	def checkfile_plus(self, verbosity=False):
		"""Checks and compare the hash sums of more than one files."""
		if not self.sumtype:
			print_error("Sumtype was not defined!\nUse --type command to define the sumtype (ex. --type sha1).")
		elif self.found:
			files_data = []
			if verbosity : print("        * Calculating Binaries *")
			with alive_bar(self.n_found, bar='blocks', spinner='dots') as bar:
				for fileid in self.found:
					if not verbosity:
						fileid.update_data(
							sumtype=self.sumtype, 
							generated_data=fileid.gen_data(bars=False)
						)
						print(fileid.checksum(self.sumtype))
					else: 
						files_data.append(list(fileid.gen_data(bars=False)))
					bar()
			if verbosity:
				for fileid, file_data in zip(self.found, files_data):
					self.checkfile(fid=fileid, fdata=file_data, bars=False)
		self.print_unfound()

	def totalcheck(self):
		"""Print all supported hash sums of one file."""
		if not self.found:
			self.print_unfound(exit=True)

		generated_datas = []
		print("        * Calculating Hashes *")
		with alive_bar(self.n_found, spinner='waves') as bar:
			for fileid in self.found:
				generated_datas.append(list(fileid.gen_data(bars=False)))
				bar()
		times = len(fileid.hlist.keys())*self.n_found
		print("        * Getting Hash Sums *")
		with alive_bar(times, spinner='waves') as bar:
			for fileid, generated_data in zip(self.found, generated_datas):
				for sumtype in fileid.hlist.keys():
					fileid.update_data(sumtype, generated_data)
					sleep(SLEEP_VALUE)
					bar()
		print("\n")

		for n, fileid in enumerate(self.found):
			if n > 0 and n < self.n_found:
				print("\n")
			print("----- '%s' -----" % fileid.name)
			for sumtype in fileid.hlist.keys():
				print(f"| {sumtype}sum: {fileid.get_hashsum(sumtype)} {fileid.name}")
			print('---------------')

		self.print_unfound()

	def print_unfound(self, exit=False):
		"""Prints all files that were not found."""
		if self.n_unfound == 1:
			print_error(f"FileNotFoundError: {self.unfound[0].name!r} was not found", exit=False)
		elif self.unfound:
			print("\nFiles that were not found or cannot be read:")
			for fileid in self.unfound:
				print(f"  -> {fileid.only_name!r}", end='')
				if fileid.dir != '.':
					print(f" in {fileid.dir}/", end='')
				print("")

		if exit : sys.exit(0)

	def write(self, name=None):
		if self.found and self.sumtype:
			textfile = name or self.sumtype + 'sum.txt'
			with open(textfile, 'w') as txt:
				for fileid in self.found:
					txt.write(f"{fileid.get_hashsum(self.sumtype)} {fileid.name}\n")
			salutations(f"\n* File: {textfile!r} Created!", sleep_time=0.064)
		else:
			print_error("Possible Causes: No Files were found or Sumtype was not defined!")
