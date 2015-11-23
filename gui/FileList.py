#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.logger import Logger

from Tools import apply_insert, apply_delete, apply_walk, insert_args, delete_args


class BaseLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)

	def show(self):
		pass

class FileLabel(GridLayout):
	@apply_insert(BaseLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_walk
	def update(self, **kwargs):
		pass

	@apply_walk
	def show(self):
		pass

class FileList(GridLayout):
	@apply_insert(FileLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_walk
	def update(self, **kwargs):
		pass

	@apply_walk
	def show(self):
		pass

class FileListApp(App):
	def build(self):
		f = FileList()
		f.insert(a=[range(4)] * 3)
		f.update(text=[['a', 'b', 'a', 'd', 'ab']] * len(f.children))
		#f.update(size_hint_y=[[.1, .2, .3, .4]] * len(f.children))
		f.update(size_hint_x=[[.2, .3, .1, .4]] * len(f.children))
		f.delete(text=[[('a', 'b'), ('a', 'c'), 'd', 'e']] * len(f.children))
		return f

if __name__ == '__main__':
	FileListApp().run()