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
except ImportError as e:
	pass

from ML.adapters.base_incomplete_model import BaseIncompleteModel
from helpers.serialization_helper import *
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

	def get_target_fw_from_model_file_name(self, file_name: str):
		file_name_parts = file_name.split('.')
		if len(file_name_parts) < 3:
			raise MindException(MindError(
				ERROR_CODE_MODEL_WRONG_FILE_NAME_FORMAT,
				'[{}]: wrong file name format for [{}] engine',
				[file_name, self.get_package_name()]
			))
		return file_name_parts[-2]

	@staticmethod
	def get_package_name():
		return 'tensorrt'

	@staticmethod
	def is_model_async():
		return True

	def get_model_from_file(self, file_name: str):
		self._model_file_content = SerializationHelper.get_model_content_from_file(
			file_name,
			self.get_package_name()
		)
		return SerializationHelper.get_sklearn_model_from_file(self._model_file_content[SKLEARN_MODEL_FILE_NAME])

	def _get_prediction(self, data):
		return self.get_model().predict(data)
