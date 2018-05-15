#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from ML.adapters.base_model import BaseModel
from helpers.serialization_helper import *
from abc import ABC, abstractmethod
import json


class BaseIncompleteModel(BaseModel):
	__model_file_content = None

	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None, **params):
		super().__init__(
			model_file=model_file,
			model=model,
			input_filters=input_filters,
			output_filters=output_filters,
			**params
		)

	def _get_input_list(self)->list:
		model_spec = json.loads(self.__model_file_content[INPUT_SPEC_FILE_NAME].read())
		return model_spec.get('inputs', [])

	@staticmethod
	def _get_input_name(model_input)->str:
		return model_input.get('name', '')

	@staticmethod
	def _get_input_type(model_input)->str:
		return model_input.get('type', '')

	@staticmethod
	def _get_input_shape(model_input) -> list:
		return model_input.get('shape', [])

	def _get_output_list(self)->list:
		model_spec = json.loads(self.__model_file_content[OUTPUT_SPEC_FILE_NAME].read())
		return model_spec.get('outputs', [])

	@staticmethod
	def _get_output_name(model_output)->str:
		return model_output.get('name', '')

	@staticmethod
	def _get_output_type(model_output)->str:
		return model_output.get('type', '')

	@staticmethod
	def _get_output_shape(model_output) -> list:
		return model_output.get('shape', [])

	@staticmethod
	@abstractmethod
	def get_package_name():
		raise NotImplementedError('you must to override this!')

	@abstractmethod
	def get_model_from_file(self, file_name: str):
		raise NotImplementedError('you must to override this!')

	@abstractmethod
	def _get_prediction(self, data):
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def is_model_async():
		raise NotImplementedError('you must to override this!')
