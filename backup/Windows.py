#-*- coding:utf-8 -*-
import thread
import time
import win32api
import win32gui
import win32con

from log import debug_log, write_log, error_log, sync


global windows_lock
windows_lock = thread.allocate_lock()

class Windows:
	active_windows = {}
	
	def __init__(self, save_time):
		self.save_time = save_time

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
		while 1:
			self.get_window()
			self.check_window()
			for key, value in self.active_windows.items():
				#print key, value
				self.send_key(key, win32con.VK_CONTROL, ord('S'))
				write_log('info', 'save file %s' % value['text'])
			time.sleep(self.save_time) #保存文件需要一定时间