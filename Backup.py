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
			target_list = handle.show(target_path)[1]
			if len(target_list):
				source_stat = get_target_name(source_file).split('#')
				target_stat = target_list[0].split('#')
				if source_stat[1:] == target_stat[1:]:
					#目录不为空且最新的备份文件与源文件相同时不备份
					return

		#备份
		target_name = get_target_name(source_file)
		handle.upload((source_file, target_name), target_path)
		target_list = handle.show(target_path)[1] #按时间顺序排列
		handle.delete(target_list[self.config.get('basic', handle.config_type, 'number'):])

	def backup_dir(self, handle, source_path, target_path):
		#遍历目录
		for source_list in Disk.walk(source_path):
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
		if Disk.isdir(source):
			target_path = '%s/%s' % (target, os.path.split(source)[1])
			self.backup_dir(handle, source, target_path)
		else:
			self.backup_file(handle, source, target)

	#运行备份
	def run_backup(self, handle, device):
		while 1:
			for backup_file in self.config.get('backup'):
				self.backup(handle, backup_file, device)
			time.sleep(self.config.get('basic', handle.config_type, 'time'))
			thread.exit_thread() #just for test

	#开启备份
	def start_backup(self, Drive):
		if self.config.get('basic', Drive.config_type, 'enable') == 'on':
			config = self.config.get('basic', Drive.config_type)
			handle = Drive(config)
			print handle.login()
			devices = handle.get_device()
			for device in devices:
				thread.start_new_thread(self.run_backup, (handle, device))


	#b.restore_file(dk, '/b/测试-.－。', 'C:/Users/zzy/Desktop/')
	#restore_cover: 恢复的文件存在是否覆盖
	#restore_time: 恢复到该时间前最后的一个备份
	def restore_file(self, handle, target_file, source_path, restore_cover=False, restore_time=9999999999):
		Disk.mkdir(source_path)
		target_list = handle.show(target_file)[1]
		#备份目录无文件则不恢复
		source_name = os.path.split(target_file)[1]
		for file_name in target_list:
			clock, md5, size = os.path.split(file_name)[1].split('#')
			if restore_time >= time.mktime(time.strptime(clock, '%Y-%m-%d@%H-%M-%S')):
				break
		else: return
		target_file = '%s/%s' % (target_file, file_name)
		if os.path.exists('%s/%s' % (source_path, source_name)):
			if not restore_cover:
				return
		#print (target_file, source_name), source_path

		handle.download((target_file, source_name), source_path)

	#从target目录恢复source文件
	def restore_dir(self, handle, target_path, source_path, restore_cover=False, restore_time=9999999999):
		for target_list in handle.restore_walk(target_path):
			for target_file in target_list[2]:
				target_child = target_list[0][len(target_path) + 1:] #子目录 
				self.restore_file(handle, '%s/%s' % (target_list[0], target_file), '%s/%s' % (source_path, target_child), restore_cover, restore_time)

	def restore(self, handle, target, source, restore_cover=False, restore_time=9999999999):
		if handle.restore_isdir(target):
			source_path = '%s/%s' % (source, os.path.split(target)[1])
			self.restore_dir(handle, target, source_path, restore_cover, restore_time)
		else:
			self.restore_file(handle, target, source, restore_cover, restore_time)


	def run(self):
		#读取配置
		self.config = Config()
		self.config.read_config()
		print self.config.config

		if not self.config.check_config(): return

		#自动保存文档
		#windows = Windows(self.config.get('basic', 'base', 'save'))
		#thread.start_new_thread(windows.save_file, ())

		#self.start_backup(Disk)
		#self.start_backup(Baidu)
		config = self.config.get('basic', Baidu.config_type)
		handle = Baidu(config)
		#self.restore_file(handle, 'F:/backup/a.doc', 'F:/', restore_cover=True)
		#self.restore_file(handle, 'F:/backup/a.doc', 'F:/', restore_cover=True, restore_time=1447127278)
		self.restore(handle, '/backup/test', 'F:/', restore_cover=True)


if __name__ == '__main__':
	backup = Backup()
	backup.run()
