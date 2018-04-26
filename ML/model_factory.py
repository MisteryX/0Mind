#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from components.mind_exception import *
from ML.adapters.keras_model import *
from ML.adapters.caffe2_model import *


class ModelFactory:
	__file_extension_to_model_map = {
		KerasModel.get_package_name(): KerasModel,
		Caffe2Model.get_package_name(): Caffe2Model
	}

	def __init__(self):
		return

	def get_model(self, model_file: str, model_type=None, input_filters=None, output_filters=None, **attributes) -> BaseModel:
		model_class = self.__get_model_class_by_file_name(model_file, model_type)
		if not model_class:
			raise MindException(
				MindError(
					MindError.CODE_UNDESCRIBED_MODEL_TYPE,
					'Model type [{}] is undescribed in the {}',
					[model_type, self.__class__.__name__]
				)
			)
		return model_class(model_file=model_file, input_filters=input_filters, output_filters=output_filters)

	def get_model_to_file_extension_dictionary(self)->dict:
		return self.__file_extension_to_model_map

	def __get_model_class_by_file_name(self, file_name: str, model_type=None)->type:
		if model_type:
			return self.get_model_to_file_extension_dictionary().get(model_type, None)
		return self.get_model_to_file_extension_dictionary().get(self.__get_file_extension(file_name), None)

	@staticmethod
	def __get_file_extension(file_name: str)->str:
		return file_name.split('.')[-1]
