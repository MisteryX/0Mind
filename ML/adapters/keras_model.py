#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

try:
	import keras
except ImportError as e:
	pass

from ML.adapters.base_model import BaseModel
from components.mind_exception import *


class KerasModel(BaseModel):
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
		return 'keras'

	@staticmethod
	def is_model_async():
		return True

	def get_model_from_file(self, file_name: str):
		return keras.models.load_model(file_name)

	def _get_input_list(self)->list:
		return self.get_model().inputs

	@staticmethod
	def _get_input_name(model_input)->str:
		return model_input.name

	@staticmethod
	def _get_input_type(model_input)->str:
		return model_input.dtype.name

	@staticmethod
	def _get_input_shape(model_input) -> list:
		return KerasModel.__get_shape_from_model(model_input)

	def _get_output_list(self)->list:
		return self.get_model().outputs

	@staticmethod
	def _get_output_name(model_output)->str:
		return model_output.name

	@staticmethod
	def _get_output_type(model_output)->str:
		return model_output.dtype.name

	@staticmethod
	def _get_output_shape(model_output) -> list:
		return KerasModel.__get_shape_from_model(model_output)

	@staticmethod
	def __get_shape_from_model(model_input_or_output)->list:
		result = []
		for dimension in model_input_or_output.shape.dims:
			result.append(dimension.value)
		return result

	def _get_prediction(self, data):
		predictions = []
		try:
			predictions = self.get_model().predict(data)
		except Exception as ex:
			self.set_error(MindError(
				ERROR_CODE_MODEL_PREDICT_RUNTIME_ERROR,
				'{}: ' + ', '.join(ex.args),
				[self.__class__.__name__]
			))
		return predictions

	def _before_predict(self, data):
		result = super()._before_predict(data)
		if len(result):
			if len(self.get_inputs()) == 1:
				return list(result.values())[0]
			return list(result.values())
		return result
