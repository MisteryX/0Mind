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
	import sklearn
except ImportError as e:
	pass

import numpy as np
from ML.adapters.base_incomplete_model import BaseIncompleteModel
from helpers.serialization_helper import *


class SKLearnModel(BaseIncompleteModel):

	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None, **params):
		super().__init__(
			model_file=model_file,
			model=model,
			input_filters=input_filters,
			output_filters=output_filters,
			**params
		)

	@staticmethod
	def get_package_name():
		return 'sklearn'

	@staticmethod
	def is_model_async():
		return False

	def get_model_from_file(self, file_name: str):
		self._model_file_content = SerializationHelper.get_model_content_from_file(
			file_name,
			self.get_package_name(),
			self.get_params()
		)
		return SerializationHelper.get_sklearn_model_from_file(self._model_file_content[SKLEARN_MODEL_FILE_NAME])

	def _before_predict(self, data):
		result = super()._before_predict(data)
		if len(result):
			if len(self.get_inputs()) == 1:
				return list(result.values())[0]
			return list(result.values())
		return result

	def _get_prediction(self, data):
		return self.get_model().predict(data)

	def _get_data_for_filter(self, data, filter_type='input'):
		if filter_type == 'input':
			return np.array(data)
		return data
