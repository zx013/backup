#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，相关设置在backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import os
import thread
import time

from Config import Config
from Windows import Windows
from Disk import Disk
from Baidu import Baidu
from tools import *
from log import debug_log, write_log


class Backup():
	#根据配置文件中的名称建立对应目录，每个文件对应以其名称命名的目录，将文件备份至该目录下
	#b.backup_file(dk, 'C:/Users/zzy/Desktop/测试-.－。', '/b')
	def backup_file(self, handle, source_file, target_path):
		#备份文件则创建对应目录
		target_path = '%s/%s' % (target_path, os.path.split(source_file)[1])
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
		handle.delete(target_list[self.config.get('basic', handle.config_type, 'number'):])

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
				self.backup_file(handle, '%s/%s' % (source_list[0], source_file), '%s/%s' % (target_path, source_child))

	#将source备份到target目录
	def backup(self, handle, source, target):
		if os.path.isdir(source):
			target_path = '%s/%s' % (target, os.path.split(source)[1])
			self.backup_dir(handle, source, target_path)
		else:
			self.backup_file(handle, source, target)

	#b.restore_file(dk, '/b/测试-.－。', 'C:/Users/zzy/Desktop/')
	def restore_file(self, handle, target_file, source_path):
		target_list = handle.show(target_file)
		#备份目录无文件则不恢复
		if not len(target_list): return

		source_name = os.path.split(target_file)[1]
		if os.path.exists('%s/%s' % (source_path, source_name)):
			i = 0
			while os.path.exists('%s/%s-restore-%s' % (source_path, source_name, i)):
				i += 1
			source_name = '%s-restore-%s' % (source_name, i)

		print (target_file, target_list[0])
		target_file = '%s/%s' % (target_file, target_list[0])
		print (target_file, source_name), source_path

		handle.download((target_file, source_name), source_path)

	#从target目录恢复source文件
	def restore(self, handle, target, source):
		pass
		
	#运行备份
	def run_backup(self, handle, device):
		while 1:
			for backup_file in self.config.get('backup'):
				self.backup(handle, backup_file, device)
			time.sleep(self.config.get('basic', handle.config_type, 'time'))

	#开启备份
	def start_backup(self, Drive):
		if self.config.get('basic', Drive.config_type, 'enable') == 'on':
			config = self.config.get('basic', Drive.config_type)
			handle = Drive(config)
			print handle.login()
			devices = handle.get_device()
			for device in devices:
				thread.start_new_thread(self.run_backup, (handle, device))
	
	def run(self):
		#读取配置
		self.config = Config()
		self.config.read_config()
		print self.config.config

		if not self.config.check_config(): return

		#自动保存文档
		#windows = Windows(self.config.get('basic', 'base', 'save'))
		#thread.start_new_thread(windows.save_file, ())

		self.start_backup(Disk)
		self.start_backup(Baidu)
		'''
		#硬盘备份
		if self.config.get('basic', 'disk', 'enable') == 'on':
			config = self.config.get('basic', Disk.config_type)
			dk1 = Disk(config)
			print dk1.login()
			for backup_file in self.config.get('backup', []):
				self.backup(dk1, backup_file, 'F:/' + config.get('path', 'backup'))

		#百度云备份
		if self.config.get('basic', 'baidu', 'enable') == 'on':
			config = self.config.get('basic', Baidu.config_type)
			dk2 = Baidu(config)
			print dk2.login()
			for backup_file in self.config.get('backup', []):
				self.backup(dk2, backup_file, '/' + config.get('path', 'backup'))
		'''

if __name__ == '__main__':
	backup = Backup()
	backup.run()
