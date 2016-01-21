#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App

from gui.mainview import MainView
from event import init_event
from event.implevent import signal


class DisplayScreen(MainView):
	def build(self):
		signal('system_init', self)

class mainApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	mainApp().run()
