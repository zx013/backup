#-*- coding:utf-8 -*-
#目前支持若干个文件的备份，备份到X:\\backup目录下的指定位置，相关设置在X:\\backup\backup.conf中配置

#异常处理
#微软office支持
#目录备份
#备份恢复
import os
import thread
import time

import win32api
import win32gui
import win32con
import win32file

from log import debug_log, write_log, error_log, sync


#备份的基本配置
scan_time = 5 #扫描时间
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


global windows_lock
windows_lock = thread.allocate_lock()

class Backup_Windows:
	active_windows = {}

	#获取窗口属性
	@sync(windows_lock)
	def EnumWindowsProc(self, hwnd, *param):
		visible = win32gui.IsWindowVisible(hwnd)
		enable = win32gui.IsWindowEnabled(hwnd) #支持鼠标键盘输入
		if visible and enable:
			self.active_windows[hwnd] = {}
			self.active_windows[hwnd]['text'] = win32gui.GetWindowText(hwnd)
			self.active_windows[hwnd]['class'] = win32gui.GetClassName(hwnd)
			self.active_windows[hwnd]['parent'] = win32gui.GetParent(hwnd)
		return True

	#获取所有可见窗口
	def get_window(self):
		self.active_windows = {}

		#目前只实现了激活窗口的按键发送，后台窗口的按键发送尚未实现
		hwnd = win32gui.GetForegroundWindow()
		self.EnumWindowsProc(hwnd, None)
		#win32gui.EnumWindows(EnumWindowsProc, None)

	#检查窗口是否为编辑器
	def check_window(self):
		for key, val in self.active_windows.items():
			if val['class'] == 'OpusApp' and 'WPS' in val['text']:
				val['type'] = 'WPS Word'
			elif val['class'] == 'XLMAIN' and 'WPS' in val['text']:
				val['type'] = 'WPS Excel'
			elif val['class'] == 'PP11FrameClass' and 'WPS' in val['text']:
				val['type'] = 'WPS PowerPoint'
			elif val['class'] == 'Notepad':
				val['type'] = 'Notepad'
			#Afx:00400000:8:00010003:00000000:000702F8
			elif 'Afx:' in val['class'] and 'UltraEdit' in val['text']:
				val['type'] = 'UltraEdit'
			else:
				#val['type'] = ''
				del self.active_windows[key]

	def send_key(self, hwnd, *keys):
		for key in keys:
			win32api.keybd_event(key, 0, 0, 0)
		for key in keys[::-1]:
			win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
		#win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
		#win32api.keybd_event(ord('S'), 0, 0, 0)
		#win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
		#win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

		#print win32gui.SetActiveWindow(hwnd)
		#print win32gui.SetForegroundWindow(hwnd)
		#print win32gui.SetFocus(hwnd)
		#print win32gui.CreateCaret(hwnd, None, 0, 0)
		#print win32gui.PostMessage(hwnd, win32con.WM_CHAR, 0x65, 0)

	#向当前激活的窗口发送Ctrl+S
	def save_file(self):
		self.get_window()
		self.check_window()
		for key, value in self.active_windows.items():
			#print key, value
			self.send_key(key, win32con.VK_CONTROL, ord('S'))


class Backup_File(Backup_Config, Backup_Windows):
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
				if number >= self.get_basic('number') or in_encode_file not in file_name:
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
			#print 'copy /Y %s %s' % (in_file, out_file)
			os.system('copy /Y %s %s 1>nul' % (in_file, out_file))

	#备份文件
	def file_backup(self):
		self.save_file()
		self.copy_file()


class Backup:
	def __init__(self, drives, drive):
		self.drives = drives
		self.drive = drive
		drives.insert_drives(drive)

	#退出备份
	def exit_backup(self):
		self.drives.delete_drives(self.drive)
		thread.exit_thread()

	#开启备份
	def start_backup(self):
		backup_file = Backup_File(self.drive)
		if not backup_file.inspect_config(): self.exit_backup()
		while 1:
			backup_file.file_backup()
			time.sleep(backup_file.get_basic('time'))

		self.exit_backup()

def run_backup():
	drives = Backup_Drives()
	while 1:
		for drive in drives.get_unactive_drives():
			backup = Backup(drives, drive)
			thread.start_new_thread(backup.start_backup, ())
		time.sleep(scan_time)

if __name__ == '__main__':
	run_backup()