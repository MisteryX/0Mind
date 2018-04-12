#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

from ML.filters.base_filter import BaseFilter
from keras.preprocessing import sequence
import numpy as np


class VectorPaddingToInputFilter(BaseFilter):

	def _apply(self):
		filtered_data = []
		if self.get_type() != 'input':
			self.get_model().set_error('filter', '{}: can be used only as an input filter'.format(self.__class__.__name__))
			return filtered_data

		inputs = self.get_model().get_inputs()
		inputs_count = len(inputs)

		if inputs_count == 1:
			input_ = inputs[0]
			filtered_data = self._get_shaped_features(input_, self.get_data()[input_['name']])
		else:
			for input_index in range(inputs_count):
				input_ = inputs[input_index]
				filtered_data.append(self._get_shaped_features(input_, self.get_data()[input_['name']]))

		return filtered_data

	@staticmethod
	def _get_shaped_features(input_, data):
		input_shape = input_['shape']
		result = np.array(data)
		if not all(isinstance(item, list) for item in data):
			batches = 1
			data_size = len(data)
			result = np.reshape(result, (batches, data_size))
		result = sequence.pad_sequences(result, maxlen=input_shape[1])
		return result

