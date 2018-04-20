#! /usr/bin/python3
# -*- coding: utf8 -*-
import argparse
import sys
import json

from ML.model_factory import ModelFactory


def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--model_file', type=str, required=True, help='ML model file path')
	parser.add_argument('-j', '--json_out', type=int, help='Force info output in JSON format', default=1)
	return parser


def show_errors(error_dict=None, json_out=True):
		if error_dict is None:
			error_dict = {}
		output = {'errors': error_dict}
		if json_out:
			print(json.dumps(output))
		else:
			print(output)


def main(params):
	model = ModelFactory().get_model(params.model_file)

	if model.has_errors():
		show_errors(model.get_errors())
		return
	spec = model.get_specification()
	if params.json_out:
		print(json.dumps(spec))
	else:
		print(spec)
	return


# --== Entry point ==--
if __name__ == "__main__":
	params_parser = create_parser()
	namespace = params_parser.parse_args(sys.argv[1:])
	main(namespace)
