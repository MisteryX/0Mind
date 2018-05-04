#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

import json
from helpers.file_helper import FileHelper

try:
	from caffe2.python import core, workspace
	from caffe2.proto.caffe2_pb2 import NetDef
except ImportError as e:
	pass

from ML.adapters.base_model import BaseModel


class Caffe2Model(BaseModel):
	__model_file_content = None

	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None):
		super().__init__(model_file=model_file, model=model, input_filters=input_filters, output_filters=output_filters)

	@staticmethod
	def get_package_name():
		return 'caffe2'

	def get_model_from_file(self, file_name: str):
		self.__model_file_content = FileHelper.get_compressed_tar_file_content(
			file_name,
			['init_net.pb', 'predict_net.pb', 'input_spec.json', 'output_spec.json']
		)
		return workspace.Predictor(self.__model_file_content['init_net.pb'], self.__model_file_content['predict_net.pb'])

	def _get_input_list(self)->list:
		model_spec = json.loads(self.__model_file_content['input_spec.json'])
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
		model_spec = json.loads(self.__model_file_content.get('output_spec.json', ''))
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

	def _get_prediction(self, data):
		return self.get_model().run(data)

	@staticmethod
	def is_model_async():
		return False
