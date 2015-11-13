#-*- coding:utf-8 -*-
import os
import shutil
from Base import Base
from tools import make_list, split_file, code
from log import debug_log, write_log, error_log

#write_log('info', 'delete %s' % file_name)
#class_name, func_name, *argv

class Disk(Base):
	config_type = 'disk'

	def __init__(self, config):
		self.config = config

	def login(self):
		return 0

	def get_device(self):
		path = self.config.get('path', 'backup')
		devices = map(lambda x: '%s:/%s' % (chr(x), path), range(65, 91))
		return filter(lambda x: os.path.exists(x), devices)

	#查看文件，按文件名排序
	@classmethod
	@error_log([[], []])
	def show(self, target_path):
		target_list = os.walk(target_path).next()
		target_dir = map(lambda x: '%s/%s' % (target_list[0], x), target_list[1][::-1])
		target_file = map(lambda x: '%s/%s' % (target_list[0], x), target_list[2][::-1])
		return target_dir, target_file

	#创建目录
	@classmethod
	def mkdir(self, target_path):
		if not os.path.exists(target_path):
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