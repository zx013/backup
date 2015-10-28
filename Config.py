#-*- coding:utf-8 -*-

class Backup_Config:
	config = {}

	def get_basic(self, key):
		return self.config['basic'].get(key)

	#读取配置文件
	def get_config(self):
		config_file = '%sbackup\\backup.conf' % self.drive
		with open(config_file, 'r') as fp:
			file_data = fp.readlines()

		self.config = {'drive': self.drive, 'basic': {}, 'file': {}}
		config_type = '' #配置类型
		for line in file_data:
			if line[0] == '#': continue
			line = line.replace('\r', '').replace('\n', '')
			if line.replace(' ', '') == '': continue
			if line[0] == '[' and line[-1] == ']':
				config_type = line[1:-1]
				continue

			data = line.split('=')
			if config_type in ('drive', 'basic'):
				self.config.setdefault(config_type)[data[0]] = data[1]
			else:
				self.config['file'].setdefault(config_type, {})[data[0]] = data[1]

		return self.config

	#检查配置文件的正确性，并设置参数默认值
	#{'drive': 'E:\\', 'file': {'C:\\Users\\zzy\\Desktop\\free%_ime.txt': {'path': 'E:\\backup\\freeime\\', 'dir': 'freeime'}}, 'basic': {'number': 10, 'time': 1}}
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