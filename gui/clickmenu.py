#-*- coding:utf-8 -*-
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, ObjectProperty

from hoverbehavior import HoverBehavior

from Tools import *

from kivy.lang import Builder
Builder.load_file('clickmenu.kv')

class ClickMenu(GridLayout):
	attach_to = ObjectProperty(None)
	_window = ObjectProperty(None, allownone=True)
	status = False #是否打开

	def __init__(self, **kwargs):
		self._parent = None
		super(ClickMenu, self).__init__(**kwargs)

	def _search_window(self):
		# get window to attach to
		window = None
		if self.attach_to is not None:
			window = self.attach_to.get_parent_window()
			if not window:
				window = self.attach_to.get_root_window()
		if not window:
			from kivy.core.window import Window
			window = Window
		return window

	def open(self, x=0, y=0):
		if self._window is not None:
			Logger.warning('ModalView: you can only open once.')
			return self
		# search window
		self._window = self._search_window()
		if not self._window:
			Logger.warning('ModalView: cannot open view, no window found.')
			return self

		if self.width + x > self._window.width:
			x = self._window.width - self.width
		
		#if self.height + y > self._window.height:
		#	y = self._window.height - self.height
		
		if y > self.height:
			y -= self.height
		
		self.pos = (x, y)
		Logger.info(str(self.pos))
		self._window.add_widget(self)

		self.status = True
		return self

	def close(self, *largs, **kwargs):
		if self._window is None:
			return self
		self._window.remove_widget(self)
		self._window = None
		self.status = False
		return self


#kv文件中根据transparent设置可见度
#selected函数实现了select（选择类型）到可见度的转换
#select类型
#0未选中，1鼠标滑过，2选中
class BackGround:
	select = 0
	color = ListProperty([0, 1, 1, 0])

	def selected(self, select):
		self.select = select
		if select == 0:
			self.color[3] = 0
		elif select == 1:
			self.color[3] = .15
		elif select == 2:
			self.color[3] = .4

class AttributeMenuLabel(Label):
	pass

class AttributeMenu(BackGround, GridLayout, HoverBehavior):
	def insert(self, **kwargs):
		label = AttributeMenuLabel(**kwargs)
		self.add_widget(label)
		#insert_args(self, **kwargs)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			return True
		super(AttributeMenu, self).on_touch_down(touch)

	def on_enter(self, *args):
		if self.select == 0:	
			self.selected(1)

	def on_leave(self, *args):
		if self.select == 1:
			self.selected(0)


class OptionMenu(BackGround, ClickMenu):
	@apply_insert(AttributeMenu)
	def insert(self, **kwargs):
		pass
