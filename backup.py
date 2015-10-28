#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，备份到X:\\backup目录下的指定位置，相关设置在X:\\backup\backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import os
import thread
import time

import win32file

from Windows import Windows
from Config import Config
from log import debug_log, write_log, error_log, sync


#备份的基本配置
scan_time = 5 #扫描时间
save_time = 10 #保存间隔
basic_time = 10 #备份间隔
basic_number = 10 #备份数量


#正在运行备份的盘
global drives_lock
drives_lock = thread.allocate_lock()

class Backup_Drives:
	active_drives = set()

	@sync(drives_lock)
	def insert_drives(self, drive):
		self.active_drives.add(drive)

	@sync(drives_lock)
	def delete_drives(self, drive):
		self.active_drives.remove(drive)

	#获取可用盘符
	def get_drives(self):
		sign = win32file.GetLogicalDrives()
		#if win32file.GetDriveType(val) == 3
		enable_drives = {val for val in {'%s:\\' % chr(ord('A') + num) for num in [i for i in range(25) if sign & 1 << i]}}
		return enable_drives

	#检查各盘是否有备份配置文件目录backup和目录下的配置文件backup.conf
	def check_backup(self, enable_drives):
		backup_drives = {drive for drive in enable_drives if os.path.exists('%sbackup\\backup.conf' % drive)}
		return backup_drives

	def get_unactive_drives(self):
		backup_drives = self.check_backup(self.get_drives()) #获取有备份配置的盘
		unactive_drives = backup_drives - self.active_drives
		return unactive_drives


class Backup_File(Backup_Config):
	def __init__(self, drive):
		self.drive = drive

	#将文件名中字符进行转义
	def encode_file(self, s):
		return ''.join(map(lambda x: x if 'a' <= x <= 'z' or 'A' <= x <= 'Z' else hex(ord(x)).replace('0x', '%'), s))

	#根据文件转义字符串恢复文件名
	def decode_file(self, s):
		return ''.join([s[0]] + map(lambda x: '%s%s' % (chr(int(x[:2], 16)), x[2:]), s.split('%')[1:]))

	#比较文件是否相同，不进行计算，直接比较修改时间
	def compare_file(self, file1, file2):
		stat1 = os.stat(file1)
		stat2 = os.stat(file2)
		if stat1[-2] != stat2[-2] or stat1[:-3] != stat2[:-3]: return False

		#计算md5反而没有直接比较快，若需要提高速度，则读取时从后往前读取
		return True

	def copy_file(self):
		for in_file, file_setting in self.config['file'].items():
			in_encode_file = self.encode_file(in_file)
			#print self.decode_file(in_encode_file)
			out_file = '%s%s@%s' % (file_setting['path'], in_encode_file, time.strftime('%Y-%m-%d@%H-%M-%S', time.localtime()))

			#获取备份的文件列表，按文件名排序
			file_list = []

			#删除超出范围和无关文件
			for number, file_name in enumerate(os.listdir(file_setting['path'])[::-1]):
				if in_encode_file not in file_name:
					os.remove('%s%s' % (file_setting['path'], file_name))
				else:
					file_list.append(file_name)

			if len(file_list) > 0:
				#当前时间小于最近备份的时间
				if out_file <= file_list[0]: continue

				#如果文件和最近的备份文件不同，则进行备份
				last_file = '%s%s' % (file_setting['path'], file_list[0])
				if self.compare_file(in_file, last_file): continue

			#in_file->out_file
			os.system('copy /Y %s %s 1>nul' % (in_file, out_file))
			write_log('info', 'copy /Y %s %s' % (in_file, out_file))
			for number, file_name in enumerate(os.listdir(file_setting['path'])[::-1]):
				if number >= self.get_basic('number'):
					os.remove('%s%s' % (file_setting['path'], file_name))


class Backup:
	def __init__(self, drives, drive):
		self.drives = drives
		self.drive = drive
		drives.insert_drives(drive)

	#退出备份
	def exit_backup(self):
		self.drives.delete_drives(self.drive)
		thread.exit_thread()
		write_log('info', 'exit %s thread' % drive)

	#开启备份
	def start_backup(self):
		backup_file = Backup_File(self.drive)
		if not backup_file.inspect_config(): self.exit_backup()
		while 1:
			backup_file.copy_file()
			time.sleep(backup_file.get_basic('time'))

		self.exit_backup()

def run_backup():
	backup_windows = Windows(save_time)
	thread.start_new_thread(backup_windows.save_file, ())
	drives = Backup_Drives()
	while 1:
		for drive in drives.get_unactive_drives():
			backup = Backup(drives, drive)
			thread.start_new_thread(backup.start_backup, ())
		time.sleep(scan_time)

if __name__ == '__main__':
	run_backup()