from collections import deque
from typing import Any
import sys, os

class Stack(object):

	def __init__(self, limit: int = None, input_type = None) -> None:
		if type(limit) is int or limit is None:
			self._limit = limit
		else:
			raise TypeError('Limit if given must be an integer value!')
		self._input_type = input_type
		self._stack_block = deque(maxlen=self._limit)
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
				self._stack_block.append(value)
			else:
				raise TypeError(f'This stack only acepts inputs of the type {str(self._input_type)}')
		return self._walk(1)

	def pop(self) -> Any:
		if not self.isempty():
			self._walk(-1)
			out = self._stack_block.pop()
			return out
		return None



class ShazamWarningHandler(Stack):
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
	def __init__(self, value: int = 1) -> None:
		super(ShazamWarningHandler, self).__init__(input_type=str)
		self._err_value = value

	def __str__(self) -> str:
		return "{} ({})".format(self.emissor, self._err_value)

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
			self.halt_execution(self._err_value)

	@classmethod
	def display_mensage(cls, msg) -> bool:
		print(f"{cls.EMISSOR}: {msg}")

	def unstack_and_halt(self):
		"""Unstack all warnings and halt the execution of this program if there
		is any warning to unstack, else it won't do anything.
		"""
		any_unstacked = False
		try:
			while (msg := self.STACK.pop()) is not None:
				self.display_mensage(msg)
				any_unstacked = True
			else:
				if any_unstacked is True:
					self.halt_execution()
		except IndexError:
			if any_unstacked is True:
				self.halt_execution()

	@classmethod
	def unstack_all(cls):
		try:
			while (msg := cls.STACK.pop()):
				cls.display_mensage(msg)
		except IndexError:
			pass

s = ShazamWarningHandler()

class GlobalWarner(ShazamWarningHandler):
	pass

class LocalWarner(ShazamWarningHandler):
	pass