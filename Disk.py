#-*- coding:utf-8 -*-
import os
import shutil
from tools import make_list, split_file, code
from log import debug_log, write_log, error_log

#write_log('info', 'delete %s' % file_name)
#class_name, func_name, *argv

class Disk:
	def get_config_type(self):
		return 'disk'

	#查看文件，按文件名排序
	def show(self, target_path):
		return os.walk(target_path).next()[2][::-1]

	def walk(self, target_path):
		return os.walk(target_path)

	#创建目录
	def mkdir(self, target_path):
		os.makedirs(target_path) #相当于linux中的mkdir -p

	#删除文件
	def delete(self, target_list):
		target_list = make_list(target_list)
		for target_file in target_list:
			if os.path.exists(target_file):
				os.remove(target_file)

	def check_path(self, target_path):
		return os.path.exists(target_path)

	#备份文件
	def upload(self, source_list, target_path):
		source_list = make_list(source_list)
		for source_file in source_list:
			source_file, source_path, source_name, target_name = split_file(source_file)
			shutil.copy(source_file, '%s/%s' % (target_path, target_name))
			#os.system('copy /Y %s %s/%s' % (source_file, target_path, target_name))

	#恢复文件
	def download(self, target_list, source_path):
		target_list = make_list(target_list)
		for target_file in target_list:
			target_file, target_path, target_name, source_name = split_file(target_file)
			shutil.copy(target_file, '%s/%s' % (source_path, source_name))
			#os.system('copy /Y %s %s/%s 1>nul' % (target_file, source_path, source_name))