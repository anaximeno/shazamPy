#!/usr/bin/env python3
""" Common is a support module, which contains the principals methods
and/or functions of this programm."""
# -*- coding: utf-8 -*-
__author__ = "Anaxímeno Brito"
__version__ = '0.4.7.1-beta'
__license__ = "GNU General Public License v3.0"
__copyright__ = "Copyright (c) 2020-2021 by " + __author__
import os
import sys
import string
import hashlib as hlib
from time import sleep
from typing import Generator, Iterable

# TODO: add type of the error when showing it, is should be one parameter of the function print_error
class Errors:
	# TODO: add errors feature?
	# TODO: Use logs when this class is called
	# TODO: Implemet the show in time feature.
	# NOTE: show in time feature should display the error message in time, if set to True, 
	# else in the end of this program execution if set to False.
	
	# Erros to be shown at the final of this program execution.
	_FINAL_ERRORS = []

	def __init__(self, to_exit: bool = True, error_type: str = 'error', error_num: int = 1, show_in_time: bool = True) -> None:
		"""if show_in_time is False, the error message will be shown at the end of the execution!
		""" # TODO: Improve this docstring!
		self._to_exit = to_exit
		self._error_num = error_num
		self._error_type = error_type
		self._show_in_time = show_in_time

	def _exit_handler(self):
		if self._to_exit is True:
			sys.exit(self._error_num)
		else:
			pass
	
	def force_exit(self, err_num: int):
		exit(err_num)

	def print_error(self, *errors: str, sep: str = '\n'):
		"""Print the error message and exit.

		Keyword args: 
			exit --> if is to exit after showing the error (default: True),
			err_num --> number of the error (default: 1)."""

		error_message = sep.join(errors)
		print(f"shazam: {self._error_type.lower()}: {error_message}")
		self._exit_handler()

	def files_not_found_error(self, files: Iterable):
		self._error_type = 'file not found error'

		if not any(files):
			pass
		elif len(files) == 1:
			self.print_error(f'{files[0].get_fullpath()!r} was not found!')
		else:
			self.print_error('files that were not found:')

			for file in files:
				print(f'  -> {file.get_fullpath()!r}')	

		self._exit_handler()

	def files_not_readable_error(self, files: Iterable):
		self._error_type = 'reading error'

		if not any(files):
			pass
		elif len(files) == 1:
			self.print_error(f'{files[0].get_fullpath()!r} is not possible to read!')
		else:
			self.print_error('some files that were not possible to read:')

			for file in files:
				print(f'  -> {file.get_fullpath()!r}')	

		self._exit_handler()


to_install = []
try:
	from termcolor import colored as clr
except ImportError:
	to_install.append('termcolor')
try:
	from tqdm import tqdm
except ImportError:
	to_install.append('tqdm')
finally:
	if any(to_install):
		modules_to_install = ' and '.join(to_install)
		modules_to_install_instructions = ' '.join(to_install)
		e = Errors(to_exit=True, error_type='module not found error')
		e.print_error(f"The package(s) {modules_to_install!r} must be installed before using the program!",
			f"\nInstall them with:\n\n\t $ pip install {modules_to_install_instructions}\n")
	else:
		del to_install


def hexa_to_int(hexa: str):
	"""Receive hexadecimal string and return integer."""
	if set(hexa).issubset(string.hexdigits):
		return int(hexa, 16)
	else:
		# TODO: to_exit should be False here below!
		e = Errors(to_exit=True, error_type='input error')
		e.print_error(f"{hexa!r} is not an hexadecimal value!")
		return None


def get_hashtype_from_string_length(string: str):
	"""Return the hashtype from the length of the string"""
	type_tab = {
		32: 'md5',
		40: 'sha1',
		56: 'sha224',
		64: 'sha256',
		96: 'sha384',
		128: 'sha512'
	}

	l = len(string)

	if l in type_tab:
		return type_tab[l]
	else:
		return None


def get_hashtype_from_filename(filename: str):
	"""Analyses the filename and return the hashtype."""
	for stype in Process.HASHTYPES_LIST[::-1]:
		if stype in filename: 
			return stype
	else:
		t = TextFile(filename)
		content = t.get_content()
		if any(content):
			return get_hashtype_from_string_length(content[0][1])
		else:
			return None


def animate(string: str, sleep_time: float = 0.1):
	for char in string:
		if char != '\n' and char != '\t':
			sleep(sleep_time)
		sys.stdout.write(char)
		sys.stdout.flush()
	print('')	# Go to new line


class File(object):
	"""This class holds all necessary informations and operations
	for one file object."""
	# Will store files that exists or not.
	Found = []
	Not_Found = []
	Unreadable = []

	def __init__(self, filename: str, given_hashsum: str = '', file_for_check: bool = True, **kwargs):
		self._file_is_for_check = file_for_check
		self._dir, self._fname = os.path.split(filename)
		if '.' in self._fname:
			self._name, self._extension = os.path.splitext(self._fname)
		else:
			self._name, self._extension = self._fname, ''

		if len(self._name) > 1 and self._name.startswith('*') and not self.exists():
			self._name = self._name[1:]

		# ´givensum´ is the original file sum which is give at the download place.
		self._gsum = given_hashsum

		# ´self._given_integer_sum´ is the integer value of the hash sum,
		# it will be used in comparisons for checking if the values are equal.
		self._given_integer_sum = hexa_to_int(self._gsum) if self._gsum else None
		if self._file_is_for_check is True:
			self._calculated_hashes = []
			self._hlist = {
				"md5": hlib.md5(),
				"sha1": hlib.sha1(),
				"sha224": hlib.sha224(),
				"sha256": hlib.sha256(),
				"sha384": hlib.sha384(),
				"sha512": hlib.sha512()
			}

			if self.exists() is True:
				if self.is_readable() is True:
					self.Found.append(self)
				else:
					self.Unreadable.append(self)
			else:
				self.Not_Found.append(self)

	def __str__(self):
		return self.get_fullpath()

	def get_name(self) -> str:
		"""Returns the name of the file without its extension, and without its the full path address."""
		return str(self._name)

	def get_extension(self) -> str:
		"""Returns the extension of the file."""
		return str(self._extension)

	def get_fullname(self) -> str:
		"""Returns the name of the file plus its extension, but without his full path address."""
		return self.get_name() + self.get_extension()

	def get_dir(self) -> str:
		"""Returns the current directory of this file."""
		return str(self._dir)

	def get_fullpath(self) -> str:
		"""Returns the full path of this file."""
		return os.path.join(self.get_dir(), self.get_fullname())

	def get_size(self) -> int:
		"""Returns the size in bytes of the file, only if it exists, else None."""
		if self.exists() is True:
			return os.path.getsize(self.get_fullpath())
		return None
	
	def get_given_sum(self) -> str:
		"""Returns the given sum of the file which will be used to compare with the calculated one, 
		for checking this file integrity."""
		return str(self._gsum)

	def exists(self) -> str:
		"""Returns if this objects exists on his directory."""
		return os.path.exists(self.get_fullpath())
	
	def is_dir(self) -> bool:
		"""Returns if this object is a directory."""
		return os.path.isdir(self.get_fullpath())

	def is_readable(self) -> bool:
		"""Returns if the file is readable or not. It must: exist on its directory, not be a directory and 
		be readable in the binary mode."""
		if not self.exists() or self.is_dir():
			return False
		try:
			with open(self.get_fullpath(), 'rb') as f:
				f.read(1)
			return True
		except UnicodeDecodeError:
			return False

	def get_hashsum(self, hashtype: str):
		"""Return the file's hash sum."""
		if hashtype in self._calculated_hashes:
			return self._hlist[hashtype].hexdigest()
		return None

	def gen_data(self, *, bar_anim: bool = True) -> Generator:
		"""Generates binary data. 
		
        Keyword arg: 
			bars_anim -- if True the function will show progress bars when generating the data.
		"""
		if self.is_readable() is False:
			e = Errors(to_exit=True)
			e.files_not_readable_error([self])

		BUF_SIZE = 32768
		times = (self.get_size() // BUF_SIZE) + (self.get_size() % BUF_SIZE)
		loop = tqdm(range(times), ncols=80, desc='CALCULATING BINARIES') if bar_anim else range(times)
		with open(self.get_fullpath(), 'rb') as f:
			for _ in loop:
				yield f.read(BUF_SIZE)
				sleep(Process.SLEEP_VALUE)	

	def update_data(self, hashtype: str, generated_data: Iterable) -> None:
		"""Updates binary data to the hashtype's class."""
		if self.is_readable() is False:
			e = Errors(to_exit=True)
			e.files_not_readable_error([self])

		for file_data in generated_data:
			self._hlist[hashtype].update(file_data)
		self._calculated_hashes.append(hashtype)

	def checksum(self, hashtype: str) -> bool:
		"""Compares file's sum with givensum and return the results"""
		return hexa_to_int(self.get_hashsum(hashtype)) == self._given_integer_sum


class TextFile(File):

	def __init__(self, filename: str, **kwargs):
		super().__init__(filename,
			given_hashsum=kwargs['given_hashsum'] if 'given_hashsum' in kwargs else '', 
			file_for_check=kwargs['file_for_check'] if 'file_for_check' in kwargs else False, 
			**kwargs)

		e = Errors(to_exit=True)
		if self.exists() is True and self.is_readable() is False:
			e.files_not_readable_error([self])
		elif self.exists() is False:
			e.files_not_found_error([self])
		else:
			pass

	def get_content(self):
		"""Return a `list with tuples` with the content of the file,
		each tuple has the following structure: ``(file name, file hash sum)``."""
		try:
			with open(self.get_fullpath(), 'rt') as textfile:
				content = [self._split_line(line) for line in textfile]
			
			return content
		except IndexError:
			e = Errors(to_exit=True, error_type='reading error')
			e.print_error(f"error reading file {self.get_fullpath()!r}:",
				 " - Each line of the file should only have the file hash sum and file name!")
		except UnicodeDecodeError:
			e = Errors(to_exit=True)
			e.files_not_readable_error([self])

		return None
	
	def _split_line(self, line: str) -> tuple:
		"""Split the line read and return the file's name and hash sum inside a tuple."""
		content = line.split()

		if not any(content) or len(content) > 2:
			raise IndexError()
		else:
			return (content[1], content[0])


class Process(object):
	# When lower is the sleep value, faster will be the reading,
	# but it will increase the CPU usage, it can be changed to
	# improve the performance.
	SLEEP_VALUE = 1e-7
	# List of all supported hash sums:
	HASHTYPES_LIST = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

	def __init__(self):
		# TODO: Check this init!!

		# ´self.found´ and ´self.unfound´ store files depending on their
		# existence/readability or not, and below them are their respective lengths.
		self._files_found = File.Found
		self._files_not_found = File.Not_Found

	def _format_file_result(self, file: File, hashtype: str):
		if file.checksum(hashtype) is True:
			color = "green"
			post_msg = 'not modified.'
		else:
			color = "red"
			post_msg = 'probably modified!!'
		return clr(f"{file.get_fullpath()!r} was {post_msg}", color)

	def checkfile(self, file: File, hashtype: str, **kwargs):
		"""Check and Compare the hash sum."""
		file_data = kwargs['file_data'] if 'file_data' in kwargs else None
		bar_anim  = kwargs['bar_anim'] if 'bar_anim' in kwargs else True
		verbosity = kwargs['verbosity'] if 'verbosity' in kwargs else True

		e = Errors(to_exit=True)
		if file.exists() is True and file.is_readable() is False:
			e.files_not_readable_error([file])
		elif file.exists() is False:
			e.files_not_found_error([file])
		else:
			pass

		file.update_data(hashtype=hashtype,
			generated_data=file_data or file.gen_data(bar_anim=bar_anim)
		)
		print(f"\n{ ' ┌──' if verbosity else '' } {self._format_file_result(file, hashtype)}")
		if verbosity:
			print(f" │ ORIGINAL {hashtype.upper()}SUM:  {file.get_given_sum()!r}")
			print(f" │ CURRENT  {hashtype.upper()}SUM:  {file.get_hashsum(hashtype)!r}")
			print(' └──────────────')

	def calculate_hash_sum(self, files: Iterable, hashtype: str, verbosity: bool = True):
		"""Calculates and prints the file's hash sum."""
		found, not_found, unreadable = self._analyse_files(files)
		
		if any(found):
			if len(found) == 1:
				file = found[0]
				file.update_data(hashtype, file.gen_data(bar_anim=True))
				print()
				if verbosity:
					print(f"{file.get_hashsum(hashtype)} {file.get_fullpath()}")
			else:
				for file in tqdm(found, desc='CALCULATING BINARIES', ncols=80):
					file.update_data(hashtype, file.gen_data(bar_anim=False))

				if verbosity:
					print()
					for file in found:
						print(f"{file.get_hashsum(hashtype)} {file.get_fullpath()}")

			if any(not_found) or any(unreadable):
				print()  # Skip one line

		e = Errors(to_exit=False)
		if any(not_found):
			e.files_not_found_error(not_found)
		if any(unreadable):
			e.files_not_readable_error(unreadable)

	def checkfiles(self, files: Iterable, hashtype: str, verbosity=False):
		"""Checks and compare the hash sums of more than one files."""
		found, not_found, unreadable = self._analyse_files(files)

		if any(found) and len(found) == 1:
			self.checkfile(found[0], hashtype, verbosity=verbosity)
		elif any(found):
			storedData = []
			for file in tqdm(found, desc='CALCULATING BINARIES', ncols=80):
				if verbosity is False:
					file.update_data(
						hashtype=hashtype, 
						generated_data=file.gen_data(bar_anim=False))
				elif verbosity is True:
					storedData.append(list(file.gen_data(bar_anim=False)))
				else:
					e = Errors(to_exit=True, error_type='internal funtion call error')
					e.print_error('verbosity in function checkfiles from common.py must be bool (True or False)!')

			if verbosity is True:
				for file, file_data in zip(found, storedData):
					self.checkfile(file, hashtype, file_data=file_data, bar_anim=False)
				print('') # new line at the end
			else:
				print('') # new line at the end
				for file in found:
					print(self._format_file_result(file, hashtype))


		e = Errors(to_exit=False)
		if any(not_found) or any(unreadable):
			print('')
			e.files_not_found_error(not_found)
			e.files_not_readable_error(unreadable)

	def totalcheck(self, files: Iterable):
		"""Print all supported hash sums of one file."""
		found, not_found, unreadable = self._analyse_files(files)

		if any(found):
			generated_datas = [
				tuple(file.gen_data(bar_anim=False)) for file in tqdm(found, ncols=71, desc='Calculating Binaries')
			]

			def update_generator():
				for file, generated_data in zip(found, generated_datas):
					for hashtype in file._hlist.keys():
						file.update_data(hashtype, generated_data)
						sleep(Process.SLEEP_VALUE)
						yield

			ug = update_generator()
			n_found = len(found)

			for _ in tqdm(range(len(found[0]._hlist.keys())*n_found), ncols=75, desc='Getting Hash Sums'):
				next(ug)
			print('\n')

			for n, file in enumerate(found):
				if n > 0 and n < n_found:
					print("\n")

				print(f" ┌── {file.get_fullname()!r}")
				for hashtype in file._hlist.keys():
					print(f" │ {hashtype}: {file.get_hashsum(hashtype)} {file.get_fullpath()}")
				print(' └────────────────────')

		e = Errors(to_exit=False)
		if any(not_found) or any(unreadable):
			e.files_not_found_error(not_found)
			e.files_not_readable_error(unreadable)

	def _analyse_files(self, files: Iterable):
		not_found = [file for file in files if not file.exists()]
		unreadable = [file for file in files if file not in not_found and not file.is_readable()]
		readable = [file for file in files if file not in unreadable and file not in not_found]

		return readable, not_found, unreadable

	def write(self, files: Iterable, hashtype: str, name: str = None):
		found, _, _ = self._analyse_files(files)
	
		if len(found) != 0:
			filename = name or (hashtype + 'sum.txt')
			with open(filename, 'wt') as txt:
				for file in found:
					txt.write(f"{file.get_hashsum(hashtype)} {file.get_fullpath()}\n")
			animate(f"\nFile {filename!r} was created!", sleep_time=0.045)			
		else:
			e = Errors('save error')
			e.print_error('there are no avaliable files for saving hash sums!')

