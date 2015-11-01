#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，相关设置在backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import os
import thread

from Config import Config
from Windows import Windows
from Disk import Disk
from log import debug_log, write_log, convert_utf8, encode_file, get_target_name

class Backup():
	#根据配置文件中的名称建立对应目录，每个文件对应以其名称命名的目录，将文件备份至该目录下
	#b.backup(dk, 'C:/Users/zzy/Desktop/测试-.－。', '/b')
	def backup(self, handle, source_file, target_path):
		#备份文件则创建对应目录
		target_path = '%s/%s' % (target_path, os.path.split(source_file)[1])
		#检查备份的目标路径
		if not handle.check_path(target_path):
			handle.mkdir(target_path)
		else:
			#有则检查路径下的内容，删除非备份文件
			target_list = handle.show(target_path)
			source_encode = encode_file(source_file)
			target_insert = [] #保留的文件
			target_delete = [] #删除的文件
			for target_file in target_list:
				if source_encode in target_file:
					target_insert.append(target_file)
				else:
					target_delete.append(target_file)
			handle.delete(target_delete)

			target_list = target_insert
			if len(target_list):
				source_stat = get_target_name(source_file).split('#')
				target_stat = target_list[0].split('#')
				target_stat[0] = os.path.split(target_stat[0])[1] #名称包含了路径
				if source_stat[0] == target_stat[0] and source_stat[2:3] == target_stat[2:3]:
					#目录不为空且最新的备份文件与源文件相同时不备份
					return

		#备份
		target_name = get_target_name(source_file)
		handle.upload((source_file, target_name), target_path)
		target_list = handle.show(target_path) #按时间顺序排列
		handle.delete(target_list[self.config.get('basic', handle.get_config_type(), 'number'):])

	def backup_file(self, handle, source_file, target_path):
		source_encode = encode_file(source_file)
		target_path = '%s/%s' % (target_path, source_encode)
		self.backup(handle, source_file, target_path)

	def backup_dir(self, handle, source_path, target_path):
		#备份文件则创建对应目录
		source_encode = encode_file(source_path)
		target_path = '%s/%s/%s' % (target_path, source_encode, os.path.split(source_path)[1])
		source_list = handle.walk(source_path)
		#遍历目录
		for source in source_list:
			source = convert_utf8(source)
			#遍历目录下文件
			for source_file in source[2]:
				self.backup(handle, '%s/%s' % (source[0], source_file), '%s/%s' % (target_path, source[0].split(source_path)[1]))

	def run(self):
		#读取配置
		self.config = Config()
		self.config.read_config()
		if not self.config.check_config(): return

		#print self.config.config

		#自动保存文档
		#windows = Windows(self.config.get('basic', 'base', 'save'))
		#thread.start_new_thread(windows.save_file, ())

		#硬盘备份
		if self.config.get('basic', 'disk', 'enable') == 'on':
			dk = Disk()
			#self.backup_file(dk, 'C:/Users/zzy/Desktop/测试-.－。', 'F:/好')
			self.backup_dir(dk, 'C:/Users/zzy/Desktop/zawu/test', 'F:/好')

		#百度云备份
		if self.config.get('basic', 'baidu', 'enable') == 'on':
			pass

if __name__ == '__main__':
	backup = Backup()
	backup.run()