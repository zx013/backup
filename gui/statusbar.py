#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from tools import *
from event.event import signal
import thread
import time

from kivy.lang import Builder
Builder.load_file('gui/statusbar.kv')


class AttributeStatusBar(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


class StatusBar(GridLayout):
	@apply_insert(AttributeStatusBar)
	def insert(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	def timer(self):
		while 1:
			signal('statusbar_timer_event', self)
			time.sleep(1)
		thread.exit_thread()

	def start_timer(self):
		thread.start_new_thread(self.timer, ())