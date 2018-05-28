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

	__target_framework = ''

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

	def __get_input_nodes(self):
		pass

	def __get_output_nodes(self):
		pass

	@staticmethod
	def __get_engine_attribues(engine_name: str)->list:
		return TRTEngineModel.__get_engine_attributes_map().get(engine_name, [])

	@staticmethod
	def get_package_name():
		return 'tensorrt'

	@staticmethod
	def is_model_async():
		return True

	def get_model_from_file(self, file_name: str):
		engine_params = self.get_params()
		if 'PLAN' not in engine_params and 'framework' not in engine_params:
			raise MindException(MindError(
				ERROR_CODE_MODEL_TRT_MISSING_COMPULSORY_ENGINE_PARAM,
				'[{}]: missing engine attribute [{}]',
				[self.__class__.__name__, 'PLAN/framework']
			))
		if 'PLAN' in engine_params:
			engine_params['PLAN'] = file_name
		elif 'framework' in engine_params:
			if 'caffe' == engine_params['framework']:
				pass
		return tensorrt.lite.Engine(**engine_params)

	def _get_prediction(self, data):
		return self.get_model().predict(data)
