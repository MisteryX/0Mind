#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from components.mind_exception import *
from helpers.validation_helper import *
from ML.adapters.base_model import BaseModel
from helpers.serialization_helper import *
from abc import ABC, abstractmethod
import json


class BaseIncompleteModel(BaseModel):
	_model_file_content = None
	_params = None

	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None, **params):
		super().__init__(
			model_file=model_file,
			model=model,
			input_filters=input_filters,
			output_filters=output_filters,
			**params
		)
		self.__close_model_files()

	def __close_model_files(self):
		if self._model_file_content:
			model_file_content = list(self._model_file_content.values())
			if model_file_content:
				model_file_content[0].close()

	def _get_io_list_from_file(self, io_spec_file_name: str, spec_type: str, error_code: int)->list:
		try:
			spec_json = ''
			if hasattr(self._model_file_content[io_spec_file_name], 'read'):
				spec_json = self._model_file_content[io_spec_file_name].read()
			model_spec = json.loads(spec_json)
		except Exception as ex:
			params = list(ex.args)
			params.insert(0, io_spec_file_name)
			params.insert(0, self.__class__.__name__)
			raise MindException(
				MindError(
					error_code,
					'{}: [{}] can not be loaded - {}',
					params
				)
			)
		return model_spec.get(spec_type, [])

	def _get_input_list(self)->list:
		if 'inputs' in self.get_params():
			inputs = self.get_params()['inputs']
		else:
			inputs = self._get_io_list_from_file(
				INPUT_SPEC_FILE_NAME,
				'inputs',
				ERROR_CODE_MODEL_INPUT_SPEC_CAN_NOT_BE_LOADED
			)
		for input_ in inputs:
			is_valid, attribute = ValidationHelper.is_dictionary_valid(input_, self.get_io_attributes())
			if not is_valid:
				raise MindException(MindError(
					ERROR_CODE_MODEL_MISSING_IO_ATTRIBUTE,
					'[{}]: missing input attribute [{}]',
					[self.__class__.__name__, attribute]
				))
		return inputs

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
		if 'outputs' in self.get_params():
			outputs = self.get_params()['outputs']
		else:
			outputs = self._get_io_list_from_file(
				OUTPUT_SPEC_FILE_NAME,
				'outputs',
				ERROR_CODE_MODEL_OUTPUT_SPEC_CAN_NOT_BE_LOADED
			)
		for output_ in outputs:
			is_valid, attribute = ValidationHelper.is_dictionary_valid(output_, self.get_io_attributes())
			if not is_valid:
				raise MindException(MindError(
					ERROR_CODE_MODEL_MISSING_IO_ATTRIBUTE,
					'[{}]: missing output attribute [{}]',
					[self.__class__.__name__, attribute]
				))
		return outputs

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

