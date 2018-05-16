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

import json
import os
from helpers.file_helper import FileHelper


INPUT_SPEC_FILE_NAME = 'input_spec.json'
OUTPUT_SPEC_FILE_NAME = 'output_spec.json'
CAFFE2_MODEL_INIT_FILE_NAME = 'init_net.pb'
CAFFE2_MODEL_PREDICT_FILE_NAME = 'predict_net.pb'
SKLEARN_MODEL_FILE_NAME = 'model.jbl'


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
		]
	}

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
	def get_list_of_model_file_content(model_type: str) -> list:
		return SerializationHelper.__model_file_content_map.get(model_type, [])

	@staticmethod
	def get_model_content_from_file(file_name: str, model_type: str):
		return FileHelper.get_compressed_tar_file_content(
			file_name,
			SerializationHelper.get_list_of_model_file_content(model_type)
		)
