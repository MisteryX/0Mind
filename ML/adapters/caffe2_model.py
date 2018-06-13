#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from helpers.serialization_helper import *

try:
	from caffe2.python import core, workspace
	from caffe2.proto.caffe2_pb2 import NetDef
except ImportError as e:
	pass

from ML.adapters.base_incomplete_model import BaseIncompleteModel


class Caffe2Model(BaseIncompleteModel):

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
		return 'caffe2'

	@staticmethod
	def is_model_async():
		return False

	def get_model_from_file(self, file_name: str):
		self._model_file_content = SerializationHelper.get_model_content_from_file(
			file_name,
			Caffe2Model.get_package_name(),
			self.get_params()
		)
		return workspace.Predictor(
			self._model_file_content[CAFFE2_MODEL_INIT_FILE_NAME].read(),
			self._model_file_content[CAFFE2_MODEL_PREDICT_FILE_NAME].read()
		)

	def _get_prediction(self, data):
		return self.get_model().run(data)

