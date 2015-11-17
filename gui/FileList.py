#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from Tools import apply_walk


class BaseLabel(Label):
	def update(self, **kwargs):
		print kwargs

	def show(self):
		pass

class FileLabel(BoxLayout):
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

class FileList(RelativeLayout):
	def refresh(self):
		pass

	def update(self, filelist):
		pass

class FileListApp(App):
	def build(self):
		f = FileLabel(length=4)
		f.update(te=['a', 'b', 'c', 'd', 'e'], ls=range(5))
		return f

if __name__ == '__main__':
	FileListApp().run()