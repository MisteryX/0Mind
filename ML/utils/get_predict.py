#! /usr/bin/python3
# -*- coding: utf8 -*-


import argparse
import json
import sys

from helpers import file_helper as fr
from ML.adapters.base_model import BaseModel
from ML.model_factory import ModelFactory


def get_params_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--model_file', type=str, required=True, help='ML model file path')
	parser.add_argument('-i', '--input_filters', type=str, required=False, help='ML model input filters pipeline', default='')
	parser.add_argument('-o', '--output_filters', type=str, required=False, help='ML model output filters pipeline', default='')
	return parser


def get_all_from_stdin():
	result = ''
	lines = sys.stdin.readlines()
	for line in range(len(lines)):
		result += lines[line].replace('\n', '')
	return result


def get_features():
	features = ''
	# Parsing features
	json_data = fr.get_text_file_content('test.json', True) #get_all_from_stdin()
	try:
		features = json.loads(json_data)
	except Exception as ex:
		BaseModel.show_errors({'features_parser': ex.args})
	return features


def main(params):
	features = get_features()
	if not features:
		return

	input_filters = None
	output_filters = None
	if len(params.input_filters):
		input_filters = json.loads(params.input_filters)
	if len(params.output_filters):
		output_filters = json.loads(params.output_filters)

	model = ModelFactory().get_model(
		model_file=params.model_file,
		input_filters=input_filters,
		output_filters=output_filters
	)
	predictions = model.predict(features)
	if model.has_errors():
		model.show_current_errors()
		return

	sys.stdout.write(json.dumps(predictions))
	return


# --== Entry point ==--
if __name__ == "__main__":
	params_parser = get_params_parser()
	namespace = params_parser.parse_args(sys.argv[1:])
	main(namespace)
