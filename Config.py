#-*- coding:utf-8 -*-
import os
from log import debug_log, convert_decode, convert_int, encode_file

class Config:
	def __init__(self):
		self.config = {'basic': {'base': {'save': 10}, 'disk': {'enable': 'on', 'path': 'backup', 'time': 10, 'number': 5}, 'baidu': {'enable': 'on', 'username': '', 'password': '', 'time': 60, 'number': 5}, 'backup': {}}}

	def get(self, *argvs):
		data = self.config
		for argv in argvs:
			data = data.get(argv)
			if data is None: return
		return data
		
	#读取配置文件
	#{'backup': {'C:\\Users\\zzy\\Desktop\\a.doc': {}, 'C:\\Users\\zzy\\Desktop\\\xb2\xe2\xca\xd4.txt': {}}, 'drive': 'a', 'basic': {'disk': {'path': 'backup', 'number': '5', 'time': '10'}, 'baidu': {'username': 'baidu_yun_test@sina.com', 'password': 'test123456', 'number': '5', 'time': '10'}, 'base': {'save': '10'}}}
	def read_config(self):
		with open('backup.conf', 'r') as fp:
			file_data = fp.readlines()

		type1 = '' #一级目录
		type2 = '' #二级目录
		for line in file_data:
			if line[0] == '#': continue
			line = line.replace('\r', '').replace('\n', '')
			if line.replace(' ', '') == '': continue
			if line[0] == '[' and line[-1] == ']':
				type1 = line[1:-1]
				self.config[type1] = {}
				continue
			if line[0] == '(' and line[-1] == ')':
				type2 = line[1:-1]
				self.config[type1][type2] = {}
				continue

			data = line.split('=')
			self.config[type1][type2][data[0]] = data[1]

	#检查配置文件的正确性
	def check_config(self):
		#转换为整数
		convert_int(self.config)

		for path, value in self.config['backup'].items():
			unicode_path = convert_decode(path, 'utf-8')
			if not os.path.exists(unicode_path):
				del self.config['backup'][path]
				debug_log('path %s not exist.' % unicode_path)
				continue
			if os.path.isfile(unicode_path):
				self.config['backup'][path]['type'] = 'file'
			elif os.path.isdir(unicode_path):
				self.config['backup'][path]['type'] = 'dir'
			else:
				del self.config['backup'][path]
				debug_log('path %s type not support.' % unicode_path)
				continue
			self.config['backup'][path]['dir'] = encode_file(path)

		#判断是否存在可备份文件
		if not len(self.config['backup']): return False

		return True