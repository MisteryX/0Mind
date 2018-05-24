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
	from sklearn.externals import joblib
except ImportError:
	pass

try:
	from caffe2.proto import caffe2_pb2
	from caffe2.python import workspace, utils, core
except ImportError:
	pass

import json
import os
from helpers.file_helper import FileHelper


INPUT_SPEC_FILE_NAME = 'input_spec.json'
OUTPUT_SPEC_FILE_NAME = 'output_spec.json'
CAFFE2_MODEL_INIT_FILE_NAME = 'init_net.pb'
CAFFE2_MODEL_PREDICT_FILE_NAME = 'predict_net.pb'
SKLEARN_MODEL_FILE_NAME = 'model.jbl'
TRT_MODEL_FILE_NAME = 'model.trt'


class SerializationHelper:

	__model_file_content_map = {
		'sklearn': [
			INPUT_SPEC_FILE_NAME,
			OUTPUT_SPEC_FILE_NAME,
			SKLEARN_MODEL_FILE_NAME
		],
		'caffe2': [
			INPUT_SPEC_FILE_NAME,
			OUTPUT_SPEC_FILE_NAME,
			CAFFE2_MODEL_INIT_FILE_NAME,
			CAFFE2_MODEL_PREDICT_FILE_NAME
		],
		'tensorrt': [
			INPUT_SPEC_FILE_NAME,
			OUTPUT_SPEC_FILE_NAME,
		]
	}

	@staticmethod
	def save_model(model_type: str, model, file_name, inputs_spec: dict, output_spec: dict):
		if 'sklearn' == model_type:
			SerializationHelper.build_sklearn_model_file(model, file_name, inputs_spec, output_spec)
		elif 'caffe2' == model_type:
			SerializationHelper.build_caffe2_model_file(model, file_name, inputs_spec, output_spec)

	@staticmethod
	def get_sklearn_model_from_file(model_file_content):
		return joblib.load(model_file_content)

	@staticmethod
	def build_sklearn_model_file(model, file_name, inputs_spec: dict, output_spec: dict):
		joblib.dump(model, SKLEARN_MODEL_FILE_NAME)
		FileHelper.write_to_file(INPUT_SPEC_FILE_NAME, json.dumps(inputs_spec))
		FileHelper.write_to_file(OUTPUT_SPEC_FILE_NAME, json.dumps(output_spec))
		FileHelper.write_files_to_tar(
			file_name + '.sklearn',
			SerializationHelper.get_list_of_model_file_content('sklearn')
		)
		os.remove(SKLEARN_MODEL_FILE_NAME)
		os.remove(INPUT_SPEC_FILE_NAME)
		os.remove(OUTPUT_SPEC_FILE_NAME)

	@staticmethod
	def build_caffe2_model_file(model, file_name, inputs_spec: dict, output_spec: dict):
		with open(CAFFE2_MODEL_PREDICT_FILE_NAME, 'wb') as f:
			f.write(model.net._net.SerializeToString())
		init_net = caffe2_pb2.NetDef()
		for param in model.params:
			op = core.CreateOperator(
				"GivenTensorFill",
				[],
				[param],
				arg=[
					utils.MakeArgument("shape", workspace.FetchBlob(param).shape),
					utils.MakeArgument("values", workspace.FetchBlob(param))
				]
			)
			init_net.op.extend([op])
		init_net.op.extend([core.CreateOperator(
				"ConstantFill",
				[],
				[inputs_spec['inputs']['0']['name']],
				shape=tuple(inputs_spec['inputs']['0']['shape'])
			)]
		)
		with open(CAFFE2_MODEL_INIT_FILE_NAME, 'wb') as f:
			f.write(init_net.SerializeToString())

		FileHelper.write_to_file(INPUT_SPEC_FILE_NAME, json.dumps(inputs_spec))
		FileHelper.write_to_file(OUTPUT_SPEC_FILE_NAME, json.dumps(output_spec))
		FileHelper.write_files_to_tar(
			file_name + '.caffe2',
			SerializationHelper.get_list_of_model_file_content('caffe2')
		)
		os.remove(CAFFE2_MODEL_INIT_FILE_NAME)
		os.remove(CAFFE2_MODEL_PREDICT_FILE_NAME)
		os.remove(INPUT_SPEC_FILE_NAME)
		os.remove(OUTPUT_SPEC_FILE_NAME)

	@staticmethod
	def get_list_of_model_file_content(model_type: str, params={}) -> list:
		result = SerializationHelper.__model_file_content_map.get(model_type, [])
		if params and 'inputs' in params:
			result.remove(INPUT_SPEC_FILE_NAME)
		if params and 'outputs' in params:
			result.remove(OUTPUT_SPEC_FILE_NAME)
		return result

	@staticmethod
	def get_model_content_from_file(file_name: str, model_type: str, params={}):
		if 'inputs' in params and 'outputs' in params:
			return {TRT_MODEL_FILE_NAME: open(file_name, 'r')}
		return FileHelper.get_compressed_tar_file_content(
			file_name,
			SerializationHelper.get_list_of_model_file_content(model_type, params)
		)
