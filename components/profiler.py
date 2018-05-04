#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

import time


class Profiler(object):
	__start_time = None

	def __init__(self):
		self.__start_time = time.time()

	def start(self):
		self.__start_time = time.time()

	def get_timing(self):
		return time.time() - self.__start_time
