#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #添加到搜索路径


import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.logger import Logger

from gui.filemanager import FileManager
from event.clickmenu_event import clickmenu_text, clickmenu_event
from event.statusbar_event import statusbar_mark, statusbar_event

from backup.config import Config

def get_filelist():
	config = Config()
	config.read_config()
	filelist = config.config['backup'].keys()

	t = []
	for f in filelist:
		if os.path.exists(f):
			f_stat= os.stat(f)
			t.append(map(str, [f.encode('utf-8'), f_stat.st_mtime, f_stat.st_dev, f_stat.st_size]))
	return t

def get_titlelabel():
	return ['名称', '修改日期', '设备', '大小']


class DisplayScreen(FileManager):
	w = [180, 180, 60, 40]
	def build(self):
		self.filelist.insert(text=get_filelist())
		self.filelist.update(width=[self.w] * len(self.filelist.children))

		self.titlelabel.insert(text=get_titlelabel())
		self.titlelabel.update(width=self.w)
		self.titlelabel.auto_sort() #自动排序

		self.filelist.click_menu.insert(text=clickmenu_text, event=clickmenu_event)

		self.statusbar.insert(mark=statusbar_mark, event=statusbar_event)
		self.statusbar.update(width=self.w)
		self.statusbar.start_timer() #启动定时器


class mainApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	mainApp().run()
