#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from modalview import ModalView
from hoverbehavior import HoverBehavior
import time

from kivy.logger import Logger

from Tools import *


class AttributeLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


class FileLabel(BackGround, GridLayout, HoverBehavior):
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
				if self.select == 0 or self.select == 1:
					self.selected(2)
				elif self.select == 2:
					self.selected(0)
			elif touch.button == 'right':
				if self.select == 0 or self.select == 1:
					for child in self.parent.children:
						if child.select:
							child.selected(0)
					self.selected(2)

	def on_enter(self, *args):
		if self.select == 0:
			self.selected(1)

	def on_leave(self, *args):
		if self.select == 1:
			self.selected(0)


class AttributeMenu(BackGround, GridLayout):
	pass

class OptionMenu(BackGround, ModalView):
	pass

class ClickMenu(GridLayout):
	def __init__(self, *args, **kwargs):
		super(ClickMenu, self).__init__(*args, **kwargs)


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

	mv = None
	def open_menu(self, x, y):
		#om = OptionMenu(pos=(0, 0), size=(100, 100))
		Logger.info(str((x, y)))
		if not self.mv:
			self.mv = OptionMenu()
		self.mv.pos=(x, y)
		self.mv.open()
		Logger.info(str([child.select for child in self.children]))

	def close_menu(self):
		if self.mv:
			self.mv.dismiss(animation=False)

	def on_touch_down(self, touch):
		super(ListLabel, self).on_touch_down(touch) #先调用子节点的事件更新select值
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				self.close_menu()
			elif touch.button == 'right':
				self.close_menu()
				self.open_menu(touch.x, touch.y)
		

class DisplayScreen(ScrollView):
	def build(self):
		f = ListLabel()
		self.add_widget(f)
		f.insert(a=[range(4)] * 32)
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