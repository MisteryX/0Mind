#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"


class ValidationHelper:

	@staticmethod
	def is_dictionary_valid(dictionary: dict, attributes: list):
		for _attribute in attributes:
			if _attribute not in dictionary:
				return False, _attribute
		return True, None

	@staticmethod
	def get_copy_of_dictionary_with_keys(dictionary: dict, keys: list) -> dict:
		return {key: dictionary[key] for key in keys if key in dictionary}

	@staticmethod
	def get_list_of_values_from_list_of_dict(list_of_dict: list, key: str) -> list:
		result = []
		for dictionary in list_of_dict:
			value = dictionary.get(key)
			if value is not None:
				result.append(value)
		return result

	@staticmethod
	def get_list_filtered_from_none(input_list: list):
		return list(filter(lambda item: item is not None, input_list))
