#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = "GNU General Public License v3.0"
__version__ = "0.4.7.4-beta"

import os
import sys
import string
import hashlib as hlib
from time import sleep
from typing import Any, Generator, Iterable, Text
from collections import deque


__author__ = "Anaxímeno J. A. Brito"
__copyright__ = "Copyright (c) 2020-2021 by " + __author__


class Stack(object):

	def __init__(self, limit: int = None, input_type = None) -> None:
		if type(limit) is int or limit is None:
			self._limit = limit
		else:
			raise TypeError('The type of the parameter argument limit must be int or None!')
		self._input_type = input_type
		self._stack = deque()
		self._top = -1

	@property
	def limit(self) -> int:
		return self._limit

	@property
	def number_of_elements(self) -> int:
		return self._top + 1

	def _walk(self, inc: int) -> bool:
		prev_top = self._top
		if type(inc) is int:
			if inc == -1:
				self._top = self._top + inc if not self.isempty() else self._top
			elif inc == 1:
				self._top = self._top + inc if not self.isfull() else self._top
			else:
				raise ValueError('The value of the parameter inc must be -1 or 1')
		else:
			raise TypeError('The type of the inc value must be int!') 
		return not self._top == prev_top


	def isfull(self) -> bool:
		return self.limit == self.number_of_elements if self.limit is not None else False

	def isempty(self) -> bool:
		return not bool(self.number_of_elements)

	def push(self, value: Any) -> bool:
		if not self.isfull():
			if self._input_type is None or type(value) is self._input_type:
				self._stack.append(value)
			else:
				raise TypeError(f'This stack only acepts inputs of the type {str(self._input_type)}')
		return self._walk(1)

	def pop(self) -> Any:
		if not self.isempty():
			self._walk(-1)
			out = self._stack.pop()
			return out
		return None



class ShazamWarningHandler:
	"""Class that displays an Error in a way it gets integrated with the program.

	Arguments:
		`name`: (str, default: 'Error') the name of the Error.

		`halt`: (bool, default: True) if set to True the program will be stoped and the Error will be shown, 
		else the Error will only be shown at the end of the execution.

		`value`: (int, default: 1) the number of the Error that will be returned to the system.
	
	Methods:
		(...)
	"""
	STACK: Stack = Stack(limit=None, input_type=str)
	EMISSOR: str = 'Shazam'
	def __init__(self, halt: bool = True,  value: int = 1) -> None:
		self._halt = halt
		self._swh_value = value
	
	def __str__(self) -> str:
		return "{} ({}), Halt: {}".format(self.emissor, self._swh_value, str(self._halt))

	def __repr__(self) -> str:
		pass

	@staticmethod
	def halt_execution(value: int = 1) -> None:
		"""Exits and returns the value parameter (default: 1) to the system."""
		sys.exit(value)

	@property
	def emissor(self) -> str:
		return str(self.EMISSOR)

	def add(self, message: str) -> None:
		"""Add an Error to the Error's stack, if the class argument `halt` was set to true, 
		the execution will be stoped and this Error will be shown else it will only be show
		at the end of the execution.
		"""
		self.STACK.push(message)
		if self._halt is True:
			self.unstack_all()
			self.halt_execution(self._swh_value)

	@classmethod
	def display_mensage(cls, msg) -> bool:
		print(f"{cls.EMISSOR}: {msg}")
	
	@classmethod
	def unstack_all(cls):
		try:
			while (msg := cls.STACK.pop()):
				cls.display_mensage(msg)
		except IndexError:
			pass


requiredPackages: list = []


try:
	from termcolor import colored as clr
except ImportError:
	requiredPackages.append("'termcolor'")
try:
	from tqdm import tqdm
except ImportError:
	requiredPackages.append("'tqdm'")
finally:
	if any(requiredPackages):
		swh = ShazamWarningHandler(halt=True, value=1)
		swh.add(f"{(', ' if len(requiredPackages) > 2 else ' and ').join(requiredPackages)}"
			f" {'are' if len(requiredPackages) > 1 else 'is'} not installed on your computer!")
	else:
		del requiredPackages


def hexa_to_int(hexa: str):
	"""Receive hexadecimal string and return integer."""
	if set(hexa).issubset(string.hexdigits):
		return int(hexa, 16)
	else:
		# TODO: to_exit should be False here below!
		swh = ShazamWarningHandler(halt=True)
		swh.add('"{}" is not an hexadecimal value!'.format(''.join(
				clr(h, 'red') if h not in string.hexdigits else h for h in hexa
			)))
		return None


def get_hashtype_from_string_length(string: str):
	"""Return the hashtype from the length of the string"""
	length_type_dict = {
		32: 'md5', 40: 'sha1', 56: 'sha224',
		64: 'sha256', 96: 'sha384', 128: 'sha512'
	}

	l = len(string)

	if l in length_type_dict:
		return length_type_dict[l]
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
			_, hashsum = content[0]
			return get_hashtype_from_string_length(hashsum)
		else:
			return None


def animate(string: str, secs: float = 0.1):
	for char in string:
		if char != '\n' and char != '\t':
			sleep(secs)
		sys.stdout.write(char)
		sys.stdout.flush()
	print('')	# Go to new line


class File(object):

	def __init__(self, filename: str, given_hashsum: str = '', file_for_check: bool = True, **kwargs):
		"""This class holds all necessary informations and operations for one file object."""
		self._swh_handler = ShazamWarningHandler(halt=True, value=1)
		
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


	def __str__(self):
		return self.fullpath

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

	@property
	def fullpath(self) -> str:
		"""Returns the full path of this file."""
		return os.path.join(self.get_dir(), self.get_fullname())

	def get_size(self) -> int:
		"""Returns the size in bytes of the file, only if it exists, else None."""
		if self.exists() is True:
			return os.path.getsize(self.fullpath)
		return None

	def get_given_sum(self) -> str:
		"""Returns the given sum of the file which will be used to compare with the calculated one,
		for checking this file integrity."""
		return str(self._gsum)

	def exists(self) -> str:
		"""Returns if this objects exists on his directory."""
		return os.path.exists(self.fullpath)

	def is_dir(self) -> bool:
		"""Returns if this object is a directory."""
		return os.path.isdir(self.fullpath)

	def is_readable(self) -> bool:
		"""Returns if the file is readable or not. It must: exist on its directory, not be a directory and
		be readable in the binary mode."""
		if not self.exists() or self.is_dir():
			return False
		try:
			with open(self.fullpath, 'rb') as f:
				f.read(1)
			return True
		except (UnicodeDecodeError, PermissionError):
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
		if not self.is_readable():
			self._swh_handler.add(f'Cannot read {self.get_fullname()}!')

		BUF_SIZE = 32768
		times = (self.get_size() // BUF_SIZE) + (self.get_size() % BUF_SIZE)
		loop = tqdm(range(times), ncols=80, desc='CALCULATING BINARIES') if bar_anim else range(times)
		with open(self.fullpath, 'rb') as f:
			for _ in loop:
				yield f.read(BUF_SIZE)
				sleep(Process.SLEEP_VALUE)

	def update_data(self, hashtype: str, generated_data: Iterable) -> None:
		"""Updates binary data to the hashtype's class."""
		if not self.is_readable():
			self._swh_handler.add(f'Cannot read {self.get_fullname()}!')

		for file_data in generated_data:
			self._hlist[hashtype].update(file_data)
		self._calculated_hashes.append(hashtype)

	def checksum(self, hashtype: str) -> bool:
		"""Compares file's sum with givensum and return the results"""
		return hexa_to_int(self.get_hashsum(hashtype)) == self._given_integer_sum


class TextFile(File):

	def __init__(self, filename: str, file_for_check: bool = False, **kwargs):
		super(TextFile, self).__init__(filename, file_for_check=file_for_check, **kwargs)

		if not self.exists():
			self._swh_handler.add(f'File {self.get_fullname()} was not found!')
		elif not self.is_readable():
			self._swh_handler.add(f'File {self.get_fullname()} is not readable!')

	def get_content(self):
		"""Return a `list with tuples` with the content of the file,
		each tuple has the following structure: ``(file name, file hash sum)``."""
		try:
			with open(self.fullpath, 'rt') as textfile:
				content = [self._split_line(line) for line in textfile]
		except IndexError:
			self._swh_handler.add(
				f"Error reading {self.fullpath}: Each line of the file must only have the file hash sum and file name, respectively."
				)
		except UnicodeDecodeError:
			self._swh_handler.add(f'File {self.get_fullname()} is not readable!')
		return content

	def _split_line(self, line: str) -> tuple:
		"""Split the line read and return the file's name and hash sum inside a tuple."""
		content = line.split()

		if not any(content) or len(content) > 2:
			raise IndexError()
		else:
			return (content[1], content[0])


class Process(object):
	SLEEP_VALUE: float = 1e-7
	HASHTYPES_LIST: list = ["md5", "sha1",
	"sha224", "sha256", "sha384", "sha512"
		]
	COLORS: dict = {
		'sucess': 'green',
		'failure': 'red'
		}
	def __init__(self):
		self._swh_handler = ShazamWarningHandler(halt=False)

	def _format_file_result(self, file: File, hashtype: str):
		if file.checksum(hashtype) is True:
			prefix = clr("-> ", self.COLORS['sucess'])
			color = self.COLORS['sucess']
			result = "not modified."
		else:
			prefix = clr("-> ", self.COLORS['failure'])
			color = self.COLORS['failure']
			result = "modified."
		return prefix + clr(f'{file.fullpath}', "white") + clr(f" was {result}", color)

	def checkfile(self, file: File, hashtype: str, **kwargs):
		"""Check and Compare the hash sum."""
		file_data = kwargs['file_data'] if 'file_data' in kwargs else None
		bar_anim  = kwargs['bar_anim'] if 'bar_anim' in kwargs else True
		verbosity = kwargs['verbosity'] if 'verbosity' in kwargs else True
		swh = ShazamWarningHandler(halt=True)
		if not file.exists():
			swh.add('File {!r} was not found!'.format(file.fullpath))
		elif not file.is_readable():
			swh.add('File {!r} is not readable!'.format(file.fullpath))

		file.update_data(hashtype=hashtype,
			generated_data=file_data or file.gen_data(bar_anim=bar_anim))
		print(f"\n{ ' ┌──' if verbosity else '' } {self._format_file_result(file, hashtype)}")
		if verbosity:
			print(f" │ O: {hashtype.upper()}SUM:  {file.get_given_sum()!r}")
			print(f" │ C: {hashtype.upper()}SUM:  {file.get_hashsum(hashtype)!r}")
			print(' └──────────────')

	def calculate_hash_sum(self, files: Iterable, hashtype: str, verbosity: bool = True):
		"""Calculates and prints the file's hash sum."""
		found, not_found, unreadable = self._analyse_files(files)
		# TODO: store file in the stack or a queue
		if any(found):
			if len(found) == 1:
				file = found[0]
				file.update_data(hashtype, file.gen_data(bar_anim=True))
				print()
				if verbosity:
					print(f"{file.get_hashsum(hashtype)} {file.fullpath}")
			else:
				for file in tqdm(found, desc='CALCULATING BINARIES', ncols=80):
					file.update_data(hashtype, file.gen_data(bar_anim=False))

				if verbosity:
					print()
					for file in found:
						print(f"{file.get_hashsum(hashtype)} {file.fullpath}")

			if any(not_found) or any(unreadable):
				print()  # Skip one line

		if any(not_found):
			self._swh_handler.add('Files that were not found: {}'.format(', '.join(f'{file.fullpath!r}' for file in not_found)))
		if any(unreadable):
			self._swh_handler.add('Could not read: {}'.format(', '.join(f'{file.fullpath!r}' for file in unreadable)))

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
				elif verbosity:
					storedData.append(list(file.gen_data(bar_anim=False)))

			if verbosity is True:
				for file, file_data in zip(found, storedData):
					self.checkfile(file, hashtype, file_data=file_data, bar_anim=False)
				print('') # new line at the end
			else:
				print('') # new line at the end
				for file in found:
					print(self._format_file_result(file, hashtype))


		print()
		if any(not_found):
			self._swh_handler.add('Files that were not found: {}'.format(', '.join(f'{file.fullpath!r}' for file in not_found)))
		if any(unreadable):
			self._swh_handler.add('Could not read: {}'.format(', '.join(f'{file.fullpath!r}' for file in unreadable)))

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
					print(f" │ {hashtype}: {file.get_hashsum(hashtype)} {file.fullpath}")
				print(' └────────────────────')

		if any(not_found):
			self._swh_handler.add('Files that were not found: {}'.format(', '.join(f'{file.fullpath!r}' for file in not_found)))
		if any(unreadable):
			self._swh_handler.add('Could not read: {}'.format(', '.join(f'{file.fullpath!r}' for file in unreadable)))

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
					txt.write(f"{file.get_hashsum(hashtype)} {file.fullpath}\n")
			animate(f"\nFile {filename!r} was created!", secs=0.045)
		# TODO: should I put else here?
