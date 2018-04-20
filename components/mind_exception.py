#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "xxxa0c@mail.ru"


class MindError:
	CODE_UNKNOWN = 0
	CODE_TASK_VALIDATION = 1
	CODE_UNSUPPORTED_MODEL_TYPE = 2
	CODE_UNDESCRIBED_MODEL_TYPE = 3

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
