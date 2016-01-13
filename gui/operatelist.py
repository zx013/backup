#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from configview import ConfigView

from tools import *


class OperateButton(Button):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


class OperateList(GridLayout):
	config_view = ConfigView()

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