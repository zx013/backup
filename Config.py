#-*- coding:utf-8 -*-
import os
from tools import convert_decode, convert_int
from log import debug_log

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
	#{'backup': {'C:\\Users\\zzy\\Desktop\\a.doc': {}, 'C:\\Users\\zzy\\Desktop\\zawu\\test': {'ignore': ['^.\\.pyc$', '^.\\.c$', '^event\\.py$', '^b(/|\\\\\\\\)c\\.txt$']}, 'C:\\Users\\zzy\\Desktop\\\xe6\xb5\x8b\xe8\xaf\x95-.\xef\xbc\x8d\xe3\x80\x82': {}}, 'basic': {'disk': {'path': 'backup', 'enable': 'on', 'number': '5', 'time': '10', 'scan': '5'}, 'baidu': {'username': 'baidu_yun_test@sina.com', 'enable': 'on', 'number': '5', 'time': '60', 'path': 'backup', 'password': 'test123456'}, 'base': {'save': '10'}}}
	def read_config(self):
		with open('backup.conf', 'r') as fp:
			file_data = fp.readlines()

		type1 = None #一级目录
		type2 = None #二级目录
		type3 = None
		for line in file_data:
			if line[0] == '#': continue
			line = line.replace('\r', '').replace('\n', '')
			if line.replace(' ', '') == '': continue
			if line[0] == '[' and line[-1] == ']':
				type1 = line[1:-1]
				type2 = None
				type3 = None
				self.config[type1] = {}
				continue
			if line[0] == '(' and line[-1] == ')':
				type2 = line[1:-1]
				type3 = None
				self.config[type1][type2] = {}
				continue
			if line[0] == '<' and line[-1] == '>':
				type3 = line[1:-1]
				self.config[type1][type2][type3] = []
				continue
			if not type1:
				continue
			elif not type2:
				conf = self.config[type1]
			elif not type3:
				conf = self.config[type1][type2]
			else:
				conf = self.config[type1][type2][type3]
				
			if line[0] == '*':
				conf.append(line[1:])
			elif '=' in line:
				data = line.split('=')
				conf[data[0]] = data[1]
		self.config = convert_decode(self.config, 'utf-8')

	#检查配置文件的正确性
	def check_config(self):
		#转换为整数
		convert_int(self.config)

		for path, value in self.config['backup'].items():
			if not os.path.exists(path):
				del self.config['backup'][path]
				debug_log('path %s not exist.' % path)
				continue
			if os.path.isfile(path):
				self.config['backup'][path]['type'] = 'file'
			elif os.path.isdir(path):
				self.config['backup'][path]['type'] = 'dir'
			else:
				del self.config['backup'][path]
				debug_log('path %s type not support.' % path)
				continue
			self.config['backup'][path]['dir'] = path

		#判断是否存在可备份文件
		if not len(self.config['backup']): return False

		return True