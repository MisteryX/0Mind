#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__maintainer__ = "Maxim Morskov"
__email__ = "0mind@inbox.ru"

from ML.filters.base_filter import BaseFilter
import numpy as np


class ArgMaxFilter(BaseFilter):
	def _apply(self):
		data = self.get_data()
		if type(data) is np.ndarray:
			return int(np.argmax(data))
		elif type(data) is list:
			return int(np.argmax(np.array(data)))
		return data
