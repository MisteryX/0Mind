#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from ML.filters.base_filter import BaseFilter
import numpy as np


class ArgMaxFilter(BaseFilter):
	def _apply(self):
		return int(np.argmax(self.get_data()))
