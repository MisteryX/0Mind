#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

try:
	import tensorrt.lite
	import uff
except ImportError as e:
	pass

from ML.adapters.base_incomplete_model import BaseIncompleteModel
from helpers.validation_helper import *
from components.mind_exception import *


class TRTEngineModel(BaseIncompleteModel):

	__target_framework = None

	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None, **params):
		super().__init__(
			model_file=model_file,
			model=model,
			input_filters=input_filters,
			output_filters=output_filters,
			**params
		)

	@staticmethod
	def __get_engine_attributes_map()->dict:
		return {
			'tf': ['framework', 'path', 'input_nodes', 'output_nodes'],
			'uff': ['framework', 'path', 'input_nodes', 'output_nodes'],
			'caffe': ['framework', 'deployfile', 'modelfile', 'input_nodes', 'output_nodes'],
			'PLAN': ['PLAN']
		}

	def _set_target_framework(self, name: str):
		self.__target_framework = name

	def get_target_framework(self)->str:
		return self.__target_framework

	def __get_input_nodes(self)->dict:
		result = {}
		for input_ in self._get_input_list():
			result[input_['name']] = tuple(input_['shape'])
		return result

	def __get_output_nodes(self)->list:
		return ValidationHelper.get_list_of_values_from_list_of_dict(self._get_input_list(), 'name')

	@staticmethod
	def __get_engine_attributes(engine_name: str)->list:
		return TRTEngineModel.__get_engine_attributes_map().get(engine_name, [])

	@staticmethod
	def get_package_name():
		return 'tensorrt'

	@staticmethod
	def is_model_async():
		return True

	def get_model_from_file(self, file_name: str):
		engine_params = self.get_params()
		if 'PLAN' in engine_params:
			self._set_target_framework('PLAN')
			engine_params['PLAN'] = file_name
		elif 'framework' in engine_params:
			self._set_target_framework(engine_params['framework'])
			engine_params['input_nodes'] = self.__get_input_nodes()
			engine_params['output_nodes'] = self.__get_output_nodes()
			if 'caffe' == engine_params['framework']:
				engine_params['modelfile'] = file_name
				if 'deployfile' not in engine_params:
					raise MindException(MindError(
						ERROR_CODE_MODEL_TRT_MISSING_ENGINE_ATTRIBUTE,
						'[{}]: missing engine attribute [{}]',
						[self.__class__.__name__, 'deployfile']
					))
			else:
				engine_params['path'] = file_name
		else:
			raise MindException(MindError(
				ERROR_CODE_MODEL_TRT_MISSING_ENGINE_ATTRIBUTE,
				'[{}]: missing engine attribute [{}]',
				[self.__class__.__name__, 'PLAN/framework']
			))
		return tensorrt.lite.Engine(**engine_params)

	def _get_prediction(self, data):
		return self.get_model().infer(data)
