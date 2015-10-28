#-*- coding:utf-8 -*-

class Config:
	def __init__(self):
		self.config = {'basic': {'base': {'save': 10}, 'disk': {'path': 'backup', 'time': 10, 'number': 5}, 'baidu': {'username': '', 'password': '', 'time': 60, 'number': 5}, 'backup': {}}

	def get_basic(self, key):
		return self.config['basic'].get(key)

	#读取配置文件
	#{'backup': {'C:\\Users\\zzy\\Desktop\\a.doc': {'dir': 'a'}, 'C:\\Users\\zzy\\Desktop\\\xb2\xe2\xca\xd4.txt': {'dir': 'freeime'}}, 'drive': 'a', 'basic': {'disk': {'path': 'backup', 'number': '5', 'time': '10'}, 'baidu': {'username': 'baidu_yun_test@sina.com', 'password': 'test123456', 'number': '5', 'time': '10'}, 'base': {'save': '10'}}}
	def get_config(self):
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
				continue
			if line[0] == '(' and line[-1] == ')':
				type2 = line[1:-1]
				continue

			data = line.split('=')
			self.config.setdefault(type1, {}).setdefault(type2, {})[data[0]] = data[1]

		return self.config

	#检查配置文件的正确性，并设置参数默认值
	def check_config(self):
		#判断目标路径是否相同
		if len({val.get('dir') for key, val in self.config['file'].items()}) != len(self.config['file']):
			debug_log('path has the same')
			return False
		#判断文件是否存在，目标路径是否为空，不存在则跳过
		for key, val in self.config['file'].items():
			in_file = key
			if os.path.exists(in_file):
				if val.get('dir').replace(' ', ''):
					out_file = '%sbackup\\%s\\' % (self.config['drive'], val['dir'])
					self.config['file'][in_file]['path'] = out_file
					if not os.path.exists(out_file):
						os.mkdir(out_file)
				else:
					debug_log('file %s path is empty' % in_file)
					del self.config['file'][key]
			else:
				debug_log('file %s not exist' % in_file)
				del self.config['file'][key]
		#判断是否存在可备份文件
		if not len(self.config['file']): return False

		#设置默认值
		self.config['basic'].setdefault('time', basic_time)
		self.config['basic']['time'] = int(self.get_basic('time'))
		self.config['basic'].setdefault('number', basic_number)
		self.config['basic']['number'] = int(self.get_basic('number'))
		return True

	def inspect_config(self):
		self.get_config()
		return self.check_config()