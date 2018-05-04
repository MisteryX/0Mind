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
from abc import ABC, abstractmethod
import ML
from helpers.file_helper import *
from ML.filters.o_default import DefaultFilter
import importlib
from importlib import util


class BaseModel(ABC):
	__errors = {}
	__description = {}
	__inputs = {}
	__outputs = {}
	__model_file = ''
	__model = None
	__input_filters = None
	__output_filters = None

	@abstractmethod
	def __init__(self, model_file='', model=None, input_filters=None, output_filters=None):
		self.clear_errors()
		self.__model_file = model_file
		self.__input_filters = {} if input_filters is None else input_filters
		self.__output_filters = {} if output_filters is None else output_filters
		if self.__model_file:
			if not self._load_model_from_file():
				return
		else:
			self.__model = model
		self._describe_model_metadata()

	def is_enabled(self):
		return importlib.util.find_spec(self.get_package_name()) is None

	def get_model(self):
		return self.__model

	def _set_model(self, model):
		self.__model = model

	def get_model_file(self):
		return self.__model_file

	def get_errors(self):
		return self.__errors

	def clear_errors(self):
		self.__errors.clear()

	def has_errors(self):
		return len(self.get_errors()) > 0

	@staticmethod
	def show_errors(error_dict=None, json_out=True):
		if error_dict is None:
			error_dict = {}
		output = {'errors': error_dict}
		if json_out:
			print(json.dumps(output))
		else:
			print(output)

	def show_current_errors(self, error_dict=None, json_out=True):
		if error_dict:
			errors = error_dict
		else:
			errors = self.get_errors()
		BaseModel.show_errors(errors, json_out)

	def get_specification(self):
		return {
			'inputs': self.get_inputs(),
			'outputs': self.get_outputs(),
			**self.get_description()
		}

	def get_description(self):
		return self.__description

	def get_inputs(self):
		return self.__inputs

	def get_outputs(self):
		return self.__outputs

	def get_input_filters(self):
		return self.__input_filters

	def get_output_filters(self):
		return self.__output_filters

	def _get_input_name_by_index(self, input_index):
		inputs = self.get_inputs()
		if input_index < 0 or input_index >= len(inputs):
			return ''
		return inputs[input_index]['name']

	def _set_input(self, key, value):
		self.__inputs[key] = value

	def _set_output(self, key, value):
		self.__outputs[key] = value

	def _set_description(self, key, value):
		self.__description[key] = value

	def set_error(self, err_type, err_message):
		self.__errors[err_type] = err_message

	def _is_input_data_valid(self, data):
		inputs = self.get_inputs()
		for input_id, input_ in inputs.items():
			if input_.get('name', '') not in data:
				self.set_error('input', 'Model input [{}] not found in the specified data'.format(input_.get('name', '')))
				return False
		return True

	def _load_model_from_file(self)->bool:
		is_file_reachable, error_message = FileHelper.is_file_reachable(self.get_model_file(), True)
		if not is_file_reachable:
			self.set_error(self.__class__.__name__, error_message)
			return False
		try:
			self._set_model(self.get_model_from_file(self.get_model_file()))
		except Exception as ex:
			self.set_error(self.__class__.__name__, ex.args)
			return False
		return True

	def _before_predict(self, data):
		result = data
		if not self._is_input_data_valid(data):
			return []
		input_filters = self.get_input_filters()
		for input_id, input_ in self.get_inputs().items():
			if input_['name'] in input_filters:
				result[input_['name']] = self._run_filters_pipeline(
					input_filters[input_['name']],
					input_id,
					data[input_['name']],
					filter_type='input'
				)
		return result

	def _after_predict(self, predictions):
		result = {}

		output_filters = self.get_output_filters()

		for output_id, output_ in self.get_outputs().items():
			__prediction = self.__get_prediction_from_model_output(predictions, output_id, output_['name'])
			if output_['name'] in output_filters and (predictions is not None and len(predictions) != 0):
				__filter = output_filters[output_['name']]
				result[output_['name']] = self._run_filters_pipeline(
					__filter,
					output_id,
					__prediction,
					filter_type='output'
				)
			else:
				result[output_['name']] = DefaultFilter(a_data=__prediction, a_input_output_id=output_id, a_model=self).apply()
		return result

	def predict(self, features):
		data = self._before_predict(features)
		if data is None or len(data) == 0:
			return
		predictions = self._get_prediction(data)
		predictions = self._after_predict(predictions)
		return predictions

	def __get_prediction_from_model_output(self, predictions, output_id: int, output: dict):
		if type(predictions) is list:
			if len(predictions) == 1:
				return predictions[0]
			elif output_id < len(predictions):
				return predictions[output_id]
			else:
				self.set_error('after_prediction', '{}: Can`t determine output id for model prediction'.format(self.__class__.__name__))
		elif type(predictions) is dict:
			if output['name'] not in predictions:
				self.set_error(
					'after_prediction',
					'{}: Can`t find output name [{}] in model prediction. Available only {}'.format(
						self.__class__.__name__,
						output['name'],
						list(predictions.keys())
					)
				)
			else:
				return predictions[output_id]
		return []

	def _describe_model_metadata(self):
		self._set_description('tool', self.get_package_name())
		self._describe_inputs()
		self._describe_outputs()

	def _run_filters_pipeline(self, filters: list, io_id: str, data, filter_type):
		result = data
		for filter_name in filters:
			filter_module, filter_class_name = ML.filters.base_filter.BaseFilter.get_module_by_filter_id(filter_name)
			try:
				filter_class = getattr(importlib.import_module('ML.filters.'+filter_module), filter_class_name)
				filter_object = filter_class(a_data=data, a_input_output_id=io_id, a_model=self, a_type=filter_type)
			except Exception as ex:
				self.set_error('filters_pipeline', 'filter name {} not found'.format(filter_name))
				return result

			if not isinstance(filter_object, ML.filters.base_filter.BaseFilter):
				self.set_error('filters_pipeline', '{} is not a regular filter'.format(filter_name))
				return result

			filter_method = getattr(filter_object, 'apply', None)
			if callable(filter_method):
				try:
					result = filter_method()
				except Exception as ex:
					self.set_error('filters_pipeline({})'.format(filter_name), ex.args)
			else:
				self.set_error('filters_pipeline({})'.format(filter_name), 'apply method not found in filter')
		return result

	def _describe_inputs(self):
		for index, model_input in enumerate(self._get_input_list()):
			self._set_input(index, {
				'name': self._get_input_name(model_input),
				'type': self._get_input_type(model_input),
				'shape': self._get_input_shape(model_input)
			})

	def _describe_outputs(self):
		for index, model_output in enumerate(self._get_output_list()):
			self._set_output(index, {
				'name': self._get_output_name(model_output),
				'type': self._get_output_type(model_output),
				'shape': self._get_output_shape(model_output)
			})

	@abstractmethod
	def _get_prediction(self, data):
		raise NotImplementedError('you must to override this!')

	@abstractmethod
	def get_model_from_file(self, file_name: str):
		raise NotImplementedError('you must to override this!')

	@abstractmethod
	def _get_input_list(self)->list:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_input_name(model_input)->str:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_input_type(model_input)->str:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_input_shape(model_input)->list:
		raise NotImplementedError('you must to override this!')

	@abstractmethod
	def _get_output_list(self) -> list:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_output_name(model_input) -> str:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_output_type(model_input) -> str:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def _get_output_shape(model_input) -> list:
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def get_package_name():
		raise NotImplementedError('you must to override this!')

	@staticmethod
	@abstractmethod
	def is_model_async():
		raise NotImplementedError('you must to override this!')

