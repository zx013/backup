#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from Tools import apply_insert, apply_walk, apply_args


class BaseLabel(Label):
	def __init__(self, **kwargs):
		super(BaseLabel, self).__init__(**kwargs)

	@apply_args
	def insert(self, **kwargs):
		pass

	@apply_args
	def update(self, **kwargs):
		pass

	def show(self):
		pass

class FileLabel(GridLayout):
	def __init__(self, **kwargs):
		super(FileLabel, self).__init__(**kwargs)

	@apply_insert(BaseLabel)
	def insert(self, **kwargs):
		pass

	@apply_walk
	def update(self, **kwargs):
		pass

	@apply_walk
	def show(self):
		pass

class FileList(GridLayout):
	def __init__(self, **kwargs):
		super(FileList, self).__init__(**kwargs)

	@apply_insert(FileLabel)
	def insert(self, **kwargs):
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
		f.insert(a=[range(3)] * 3)
		f.update(text=[('a', 'b', 'c', 'd')] * len(f.children))
		#f.update(size_hint_y=[(.1, .2, .3, .4)] * len(f.children))
		f.update(size_hint_x=[(.2, .3, .1, .4)] * len(f.children))
		return f

if __name__ == '__main__':
	FileListApp().run()