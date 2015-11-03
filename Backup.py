#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，相关设置在backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import thread

from Config import Config
from Windows import Windows
from Disk import Disk
from Baidu import Baidu
from path import *
from log import debug_log, write_log, get_target_name


class Backup():
	#根据配置文件中的名称建立对应目录，每个文件对应以其名称命名的目录，将文件备份至该目录下
	#b.backup(dk, 'C:/Users/zzy/Desktop/测试-.－。', '/b')
	def backup(self, handle, source_file, target_path):
		#备份文件则创建对应目录
		target_path = '%s/%s' % (target_path, split(source_file)[1])
		#检查备份的目标路径
		if not handle.check_path(target_path):
			handle.mkdir(target_path)
		else:
			target_list = handle.show(target_path)
			if len(target_list):
				source_stat = get_target_name(source_file).split('#')
				target_stat = target_list[0].split('#')
				if source_stat[1:] == target_stat[1:]:
					#目录不为空且最新的备份文件与源文件相同时不备份
					return

		#备份
		target_name = get_target_name(source_file)
		handle.upload((source_file, target_name), target_path)
		target_list = handle.show(target_path) #按时间顺序排列
		handle.delete(target_list[self.config.get('basic', handle.get_config_type(), 'number'):])

	def backup_file(self, handle, source_file, target_path):
		self.backup(handle, source_file, target_path)

	def backup_dir(self, handle, source_path, target_path):
		#遍历目录
		for source_list in walk(source_path):
			#遍历目录下文件
			for source_file in source_list[2]:
				#跳过忽略的文件
				source_child = source_list[0][len(source_path) + 1:] #子目录
				if source_child:
					source_name = '%s/%s' % (source_child, source_file)
				else:
					source_name = source_file
				if search(self.config.get('backup', source_path, 'ignore'), source_name):
					continue
				self.backup(handle, '%s/%s' % (source_list[0], source_file), '%s/%s' % (target_path, source_child))

	def backup_data(self, handle, source, target):
		if isdir(source):
			target_path = '%s/%s' % (target, split(source)[1])
			self.backup_dir(handle, source, target_path)
		else:
			self.backup_file(handle, source, target)
	
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
			#self.backup_dir(dk, 'C:\\Users\\zzy\\Desktop\\zawu\\test', 'F:\\好')
			self.backup_data(dk, 'C:\\Users\\zzy\\Desktop\\zawu\\server.c', 'E:/backup')
			self.backup_data(dk, 'C:\\Users\\zzy\\Desktop\\zawu\\Windows程序设计', 'E:/backup')

		#百度云备份
		if self.config.get('basic', 'baidu', 'enable') == 'on':
			dk = Baidu(self.config.get('basic', 'baidu', 'username'), self.config.get('basic', 'baidu', 'password'))
			#print dk.login()
			#self.backup_file(dk, 'C:/Users/zzy/Desktop/测试-.－。', '/b')
			#self.backup_dir(dk, 'C:/Users/zzy/Desktop/zawu/test', '/b')

if __name__ == '__main__':
	backup = Backup()
	backup.run()
