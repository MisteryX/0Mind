#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"


ERROR_CODE_UNKNOWN = 0
ERROR_CODE_TASK_VALIDATION = 1
ERROR_CODE_MODEL_UNSUPPORTED_TYPE = 2
ERROR_CODE_MODEL_UNDESCRIBED_TYPE = 3
ERROR_CODE_MODEL_INPUT_NOT_FOUND_IN_DATA = 4
ERROR_CODE_MODEL_FILE_IS_UNREACHABLE = 5
ERROR_CODE_MODEL_LOAD_FAIL = 6
ERROR_CODE_MODEL_OUTPUT_NOT_FOUND = 7
ERROR_CODE_MODEL_OUTPUT_NAME_NOT_FOUND = 8
ERROR_CODE_MODEL_PREDICT_RUNTIME_ERROR = 9
ERROR_CODE_MODEL_INPUT_SPEC_CAN_NOT_BE_LOADED = 10
ERROR_CODE_MODEL_OUTPUT_SPEC_CAN_NOT_BE_LOADED = 11
ERROR_CODE_MODEL_WRONG_FILE_NAME_FORMAT = 12
ERROR_CODE_MODEL_TRT_MISSING_ENGINE_ATTRIBUTE = 13
ERROR_CODE_MODEL_MISSING_IO_ATTRIBUTE = 14
ERROR_CODE_FILTER_WRONG_TYPE = 50
ERROR_CODE_FILTER_WRONG_PARAMS = 51
ERROR_CODE_FILTER_FILE_IS_UNREACHABLE = 52
ERROR_CODE_FILTER_NOT_FOUND = 53
ERROR_CODE_FILTER_WRONG_INTERFACE = 54
ERROR_CODE_FILTER_RUNTIME_ERROR = 55
ERROR_CODE_REQUEST_ATTRIBUTES_VALIDATION = 100
ERROR_CODE_REQUEST_WRONG_CONTENT_TYPE = 101
ERROR_CODE_REQUEST_MODEL_LOAD_HAS_NO_DATA = 102
ERROR_CODE_REQUEST_MODEL_HAS_BEEN_ALREADY_LOADED = 103
ERROR_CODE_REQUEST_UNKNOWN_LOAD_MODEL_ERROR = 104
ERROR_CODE_REQUEST_WRONG_DATA_IS_EMPTY = 105
ERROR_CODE_REQUEST_NO_IDLE_MODELS_FOR_PREDICT = 106
ERROR_CODE_REQUEST_UNKNOWN_PREDICT_ERROR = 107
ERROR_CODE_REQUEST_MODEL_NOT_FOUND = 108
ERROR_CODE_REQUEST_WRONG_POOL_ID_FOR_STOP_COMMAND = 109


class MindError:

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
			'message': (self.get_message()).format(*self.get_params()),
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

	def __init__(self, error=None, previous_errors=list(), *args, **kwargs):
		super().__init__(self, *args, **kwargs)

		self.__previous_errors = previous_errors
		self.__error = error

	def get_error(self)->MindError:
		return self.__error

	def get_previous_errors(self)->list:
		return self.__previous_errors

	def get_errors(self)->list:
		error_list = self.__previous_errors
		if self.__error:
			error_list.append(self.__error)
		return error_list
