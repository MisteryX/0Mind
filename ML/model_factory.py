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
from helpers.module_helper import ModuleHelper
from helpers.file_helper import FileHelper
from ML.adapters.base_model import BaseModel


class ModelFactory:
	__file_extension_to_model_map = {
		'keras': {
			'model': 'KerasModel',
			'module': 'ML.adapters.keras_model',
		},
		'caffe2': {
			'model': 'Caffe2Model',
			'module': 'ML.adapters.caffe2_model',
		},
		'sklearn': {
			'model': 'SKLearnModel',
			'module': 'ML.adapters.sklearn_model'
		},
		'tensorrt': {
			'model': 'TRTEngineModel',
			'module': 'ML.adapters.trt_engine_model'
		}
	}

	def __init__(self):
		return

	def get_model(
			self,
			id: str,
			model_file: str,
			model_type=None,
			input_filters=None,
			output_filters=None,
			**params
	)->BaseModel:
		model_class = self.__get_model_class_by_file_name(model_file, model_type)
		if not model_class:
			raise MindException(
				MindError(
					ERROR_CODE_MODEL_UNDESCRIBED_TYPE,
					'Model type [{}] is undescribed in the {}',
					[model_type, self.__class__.__name__]
				)
			)
		return model_class(id=id, model_file=model_file, input_filters=input_filters, output_filters=output_filters, **params)

	def get_model_to_file_extension_dictionary(self)->dict:
		return self.__file_extension_to_model_map

	def __get_model_class_by_file_name(self, file_name: str, model_type=None)->type:
		_model_type = model_type if model_type else FileHelper.get_file_extension(file_name)
		_model_type_map = self.get_model_to_file_extension_dictionary().get(_model_type, None)
		if not _model_type_map:
			return None
		return ModuleHelper.get_class_for(_model_type_map['module'], _model_type_map['model'])

