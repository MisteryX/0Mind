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

from ML.adapters.base_model import BaseModel
from components.mind_exception import *


class SKLearnModel(BaseModel):
	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None):
		super(SKLearnModel, self).__init__(model_file=model_file, model=model, input_filters=input_filters, output_filters=output_filters)

	@staticmethod
	def get_package_name():
		return 'sklearn'

	@staticmethod
	def is_model_async():
		return False

	def get_model_from_file(self, file_name: str):
		pass

	def _get_input_list(self)->list:
		pass

	@staticmethod
	def _get_input_name(model_input)->str:
		pass

	@staticmethod
	def _get_input_type(model_input)->str:
		pass

	@staticmethod
	def _get_input_shape(model_input) -> list:
		pass

	def _get_output_list(self)->list:
		pass

	@staticmethod
	def _get_output_name(model_output)->str:
		pass

	@staticmethod
	def _get_output_type(model_output)->str:
		pass

	@staticmethod
	def _get_output_shape(model_output) -> list:
		pass

	@staticmethod
	def __get_shape_from_model(model_input_or_output)->list:
		pass

	def _get_prediction(self, data):
		pass

	def _before_predict(self, data):
		result = super()._before_predict(data)
		pass
		return result