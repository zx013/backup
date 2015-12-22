#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from tools import *

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