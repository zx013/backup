#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from Tools import apply_walk, apply_args


class BaseLabel(Label):
	def __init__(self, **kwargs):
		super(BaseLabel, self).__init__(**kwargs)

	@apply_args
	def update(self, **kwargs):
		pass

	def show(self):
		pass

class FileLabel(GridLayout):
	def __init__(self, **kwargs):
		super(FileLabel, self).__init__(**kwargs)
		self.data = kwargs
		for i in xrange(kwargs.get('length', 0)):
			baselabel = BaseLabel()
			self.add_widget(baselabel)

	@apply_walk
	def update(self, **kwargs):
		pass

	@apply_walk
	def show(self):
		pass

class FileList(GridLayout):
	def __init__(self, **kwargs):
		super(FileList, self).__init__(**kwargs)
		for i in xrange(kwargs.get('length', 0)):
			filelabel = FileLabel(length=4)
			self.add_widget(filelabel)

	@apply_walk
	def update(self, **kwargs):
		pass

	@apply_walk
	def show(self):
		pass

class FileListApp(App):
	def build(self):
		f = FileList(length=3)
		f.update(text=[('a', 'b', 'c', 'd')] * len(f.children))
		#f.update(size_hint_y=[(.1, .2, .3, .4)] * len(f.children))
		f.update(size_hint_x=[(.2, .3, .1, .4)] * len(f.children))
		return f

if __name__ == '__main__':
	FileListApp().run()