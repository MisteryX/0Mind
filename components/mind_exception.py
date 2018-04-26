#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"


class MindError:
	CODE_UNKNOWN = 0
	CODE_TASK_VALIDATION = 1
	CODE_MODEL_UNSUPPORTED_TYPE = 2
	CODE_MODEL_UNDESCRIBED_TYPE = 3
	CODE_MODEL_INPUT_NOT_FOUND_IN_DATA = 4
	CODE_MODEL_FILE_IS_UNREACHABLE = 5
	CODE_MODEL_LOAD_FAIL = 6
	CODE_MODEL_OUTPUT_NOT_FOUND = 7
	CODE_MODEL_OUTPUT_NAME_NOT_FOUND = 8
	CODE_MODEL_PREDICT_RUNTIME_ERROR = 9
	CODE_FILTER_WRONG_TYPE = 50
	CODE_FILTER_WRONG_PARAMS = 51
	CODE_FILTER_FILE_IS_UNREACHABLE = 52
	CODE_FILTER_NOT_FOUND = 53
	CODE_FILTER_WRONG_INTERFACE = 54
	CODE_FILTER_RUNTIME_ERROR = 55
	CODE_REQUEST_ATTRIBUTES_VALIDATION = 100
	CODE_REQUEST_WRONG_CONTENT_TYPE = 101
	CODE_REQUEST_MODEL_LOAD_HAS_NO_DATA = 102
	CODE_REQUEST_MODEL_HAS_BEEN_ALREADY_LOADED = 103
	CODE_REQUEST_UNKNOWN_LOAD_MODEL_ERROR = 104

	def __init__(self, code: int, message: str, params: list):
		self.__code = code
		self.__message = message
		self.__params = params

	def get_code(self)->int:
		return self.__code

	def get_message(self)->str:
		return self.__message

	def get_params(self)->list:
		return self.__params

	def get_as_dict(self)->dict:
		return {
			'code': self.get_code(),
			'message': self.get_message(),
			'params': self.get_params()
		}

	@staticmethod
	def get_as_json_serializable(errors: list):
		result = []
		for error in errors:
			result.append(error.get_as_dict())
		return result


class MindException(RuntimeError):
	__previous_errors = None
	__error = None

	def __init__(self, error: MindError, previous_errors=list(), *args, **kwargs):
		super().__init__(self, *args, **kwargs)

		self.__previous_errors = previous_errors
		self.__error = error

	def get_error(self)->MindError:
		return self.__error

	def get_previous_errors(self)->list:
		return self.__previous_errors

	def get_errors(self)->list:
		error_list = self.__previous_errors
		error_list.append(self.__error)
		return error_list
