#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from tools import *

from kivy.lang import Builder
Builder.load_file('gui/operatelist.kv')

class OperateButton(Button):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			if hasattr(self, 'event'):
				if hasattr(self.event, '__call__'):
					self.event(self)
		super(OperateButton, self).on_touch_down(touch)


class OperateList(GridLayout):
	@apply_insert(OperateButton)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	@apply_destroy
	def destroy(self, **kwargs):
		pass