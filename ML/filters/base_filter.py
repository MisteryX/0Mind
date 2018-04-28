#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from abc import ABC, abstractmethod


class BaseFilter(ABC):
	_type = None
	_data = None
	_model = None
	_input_output_id = None

	'''
	Constructor
	
	@param a_model: AbstractMLModel
	'''
	def __init__(self, a_data, a_input_output_id: str, a_model, a_type='input'):
		self._type = a_type
		self._data = a_data
		self._model = a_model
		self._input_output_id = a_input_output_id

	def get_type(self):
		return self._type

	def get_data(self):
		return self._data

	def get_model(self):
		return self._model

	def get_io_id(self):
		return self._input_output_id

	def apply(self):
		result = self._data
		if self._before_apply():
			result = self._apply()
		return self._after_apply(result)

	@abstractmethod
	def _apply(self):
		pass

	def _before_apply(self)->bool:
		return len(self._data) != 0

	def _after_apply(self, result):
		return result

	@staticmethod
	def get_module_by_filter_id(a_filter_id: str)->tuple:
		return tuple(a_filter_id.split('.'))
