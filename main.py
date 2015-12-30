#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App

from gui.filemanager import FileManager
from event import init_event, event


class DisplayScreen(FileManager):
	def build(self):
		event.signal('system_init', self)


class mainApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	mainApp().run()
