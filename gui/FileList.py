#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView 

from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Rectangle

from kivy.logger import Logger

from Tools import *


class AttributeLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


class FileLabel(GridLayout):
	select = False
	rect = None

	def selected(self):
		if not self.rect:
			with self.canvas:
				Color(rgba=(0, 1, 1, .3))
				self.rect = Rectangle(size=self.size)

		if self.select:
			self.rect.pos = self.pos
		else:
			self.rect.pos = -1000, -1000

	@apply_insert(AttributeLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	def on_touch_down(self, touch):
		#如果选中则直接打开选项栏
		#如果未选中则清空其它选项并选择该项，然后打开选项栏
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				self.select = not self.select
				self.selected()
			elif touch.button == 'right':
				if not self.select:
					for child in self.parent.children:
						if child.select:
							child.select = False
							child.selected()
					self.select = True
				self.selected()
				


class ListLabel(GridLayout):
	@apply_insert(FileLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass


class DisplayScreen(ScrollView):
	def build(self):
		f = ListLabel()
		self.add_widget(f)
		f.insert(a=[range(4)] * 28)
		t = []
		for i in range(len(f.children)):
			t.append(['a%s' % i, 'b', 'a', 'd', 'ab'])
		f.update(text=t)
		f.update(size_hint_x=[[.2, .3, .1, .4]] * len(f.children))
		#f.delete(text=[[('a', 'b'), ('a', 'c'), 'd', 'e']] * len(f.children))
		#f.draw()
		f.bind(minimum_height=f.setter('height'))


class FileListApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	FileListApp().run()