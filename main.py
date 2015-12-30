#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #添加到搜索路径


import kivy
kivy.require('1.9.0')

from kivy.app import App

from gui.filemanager import FileManager
import event.clickmenu_event
import event.filelist_event
import event.titlelabel_event
import event.statusbar_event
from event.event import signal


class DisplayScreen(FileManager):
	def build(self):
		signal('clickmenu_init', self)
		signal('filelist_init', self)
		signal('titlelabel_init', self)
		signal('statusbar_init', self)


class mainApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	mainApp().run()
