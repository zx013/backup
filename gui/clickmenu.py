#-*- coding:utf-8 -*-
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, ObjectProperty

from hoverbehavior import HoverBehavior

from Tools import *

from kivy.lang import Builder
Builder.load_file('clickmenu.kv')


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

class AttributeMenu(Label):
	def __init__(self, **kwargs):
		super(AttributeMenu, self).__init__(**kwargs)

class OptionMenu(BackGround, GridLayout, HoverBehavior):
	clickmenu = None #下一级菜单

	def insert(self, **kwargs):
		text = kwargs.get('text')
		#可以继续扩展
		if isinstance(text, tuple) or isinstance(text, list):
			self.clickmenu = ClickMenu()
			kwargs['text'] = text[1:]
			self.clickmenu.insert(**kwargs)
			kwargs['text'] = text[0]
		label = AttributeMenu(**kwargs)
		self.add_widget(label)
		#insert_args(self, **kwargs)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			return True
		super(OptionMenu, self).on_touch_down(touch)

	#进入子菜单时主菜单不关闭clickmenu
	def on_enter(self, *args):
		if self.select == 0:
			for child in self.parent.children:
				if child.select == 1:
					child.selected(0)
					if child.clickmenu:
						child.clickmenu.close()
			self.selected(1)
		if self.clickmenu:
			self.clickmenu.open(self.x + self.width - 3, self.y + self.height)

	def on_leave(self, *args):
		#if self.select == 1:
			#self.selected(0)
		if self.clickmenu:
			child_select = [child.select for child in self.clickmenu.children]
			if 1 not in child_select:
				self.clickmenu.close()
				self.selected(0)
		else:
			self.selected(0)


class ClickMenu(GridLayout, HoverBehavior):
	@apply_insert(OptionMenu)
	def insert(self, **kwargs):
		pass

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
		#Logger.info(str(self.pos))
		self._window.add_widget(self)

		self.status = True
		return self

	def close(self, *largs, **kwargs):
		#递归关闭所有节点
		for child in self.children:
			if child.clickmenu:
				child.clickmenu.close()

		if self._window is None:
			return self
		self._window.remove_widget(self)
		self._window = None
		self.status = False
		return self