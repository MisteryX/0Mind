#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

import sys
import importlib
import importlib.util


class ModuleHelper:

	def __init__(self):
		return

	@staticmethod
	def get_class_for(module_name: str, class_name: str):
		module_spec = importlib.util.find_spec(module_name)
		if module_spec is None:
			return None
		if module_name not in sys.modules:
			_module = importlib.import_module(module_name)
		else:
			_module = sys.modules[module_name]

		_class = getattr(_module, class_name)
		return _class
