#! /usr/bin/python3
# -*- coding: utf8 -*-
__author__ = "Maxim Morskov"
__copyright__ = "Copyright 2017, Maxim Morskov"
__credits__ = ["Maxim Morskov"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Maxim Morskov"
__site__ = "http://0mind.net"

import sys
import os
import os.path
import tarfile


class FileHelper:
	@staticmethod
	def is_file_reachable(file_name, quiet=False):
		if not os.path.isfile(file_name) or not os.access(file_name, os.R_OK):
			error_message = 'File [{}] not found or can`t be reached'.format(file_name)
			if not quiet:
				print(error_message)
				return False, ''
			else:
				return False, error_message
		return True, ''

	@staticmethod
	def get_text_file_content(file_name, quiet=False):
		if not FileHelper.is_file_reachable(file_name, quiet):
			return
		with open(file_name, 'r') as m_file:
			data = m_file.read().replace('\n', '')
			m_file.close()
		return data

	@staticmethod
	def get_compressed_tar_file_content(file_name: str, files_list: list, mode='r:gz')->dict:
		result = {}
		with tarfile.open(file_name, mode) as tar:
			for compressed_file_name in files_list:
				file_gz = tar.getmember(compressed_file_name)
				uncompressed_file = tar.extractfile(file_gz)

				if uncompressed_file is None:
					raise Exception("Can`t extract file {} from {} archive".format(compressed_file_name, file_name))
				result[compressed_file_name] = uncompressed_file.read()
		return result

	@staticmethod
	def get_text_file_lines(file_name, quiet=False):
		if not FileHelper.is_file_reachable(file_name, quiet):
			return []
		with open(file_name) as m_file:
			content = m_file.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip() for x in content]
		return content

	@staticmethod
	def write_to_file(file_name: str, body: str):
		_file = open(file_name, 'w')
		result = _file.write(body)
		_file.close()
		return result


# --== Entry point ==--
if __name__ == "__main__":
	if len(sys.argv) >= 2:
		print(FileHelper.get_text_file_content(sys.argv[1]))
