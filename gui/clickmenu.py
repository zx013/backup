#-*- coding:utf-8 -*-
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, ObjectProperty

from hoverbehavior import HoverBehavior

from tools import *

from kivy.lang import Builder
Builder.load_file('clickmenu.kv')


#kv文件中根据transparent设置可见度
#selected函数实现了select（选择类型）到可见度的转换
#select类型
#0未选中，1鼠标滑过，2选中
class BackGround:
	select = 0
	space_color = ListProperty([0, .6, 1, 0])
	frame_color = ListProperty([0, .6, 1, 0])

	def selected(self, select):
		self.select = select
		if select == 0:
			self.space_color[3] = 0
			self.frame_color[3] = 0
		elif select == 1:
			self.space_color[3] = .1
			self.frame_color[3] = .4
		elif select == 2:
			self.space_color[3] = .3
			self.frame_color[3] = .6

class AttributeMenu(Label):
	pass

class OptionMenu(BackGround, GridLayout, HoverBehavior):
	click_menu = None #下一级菜单
	click_event = None

	def insert(self, **kwargs):
		if not self.click_menu:
			self.click_menu = ClickMenu()
			self.click_menu.parent_menu = self.parent #设置父菜单

		args = {} #缓存
		for key, value in kwargs.items():
			if isinstance(value, tuple) or isinstance(value, list):
				kwargs[key] = value[1:]
				args[key] = value[0]
		if args:
			self.click_menu.insert(**kwargs)
		for key, value in args.items():
			kwargs[key] = value

		label = AttributeMenu(**kwargs)
		self.add_widget(label)
		self.click_event = kwargs.get('event')

	#捕捉点击事件，使其后控件的事件不生效
	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			return True
		super(OptionMenu, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if self.collide_point(touch.x, touch.y):
			if hasattr(self.click_event, '__call__'):
				self.click_event()
			return True
		super(OptionMenu, self).on_touch_up(touch)

	def click(self):
		if self.click_menu:
			self.click_menu.open(self.pos, open_type='enter', size=self.size)

	#递归判断点是否在子控件中
	def collide(self, child_menu, x, y):
		if child_menu:
			if child_menu.collide_point(x, y):
				return True
			return self.collide(child_menu.child_menu, x, y)
		return False

	def on_enter(self, *args):
		#进入父控件时在子控件中
		if self.parent.child_menu:
			if self.collide(self.parent.child_menu, self.border_point[0], self.border_point[1]):
				return
			self.parent.child_menu.close()

		#清空同级菜单select值
		for child in self.parent.children:
			if child.select == 1:
				child.selected(0)
		if self.select == 0:
			self.selected(1)
		self.click()

	def on_leave(self, *args):
		#离开子控件时在其子控件中
		if self.parent.child_menu:
			if self.collide(self.parent, self.border_point[0], self.border_point[1]):
				return

		#离开子控件时在父控件中
		if self.parent.parent_menu:
			if self.parent.parent_menu.collide_point(self.border_point[0], self.border_point[1]): #在父控件内
				self.parent.close()
				#清空同级菜单select值
				for child in self.parent.parent_menu.children:
					if child.select == 1:
						child.selected(0)
				#获取所在控件
				for child in self.parent.parent_menu.children:
					if child.collide_point(self.border_point[0], self.border_point[1]):
						if child.select == 0:
							child.selected(1)
						child.click()
						break


class ClickMenu(GridLayout):
	@apply_insert(OptionMenu)
	def insert(self, **kwargs):
		pass

	attach_to = ObjectProperty(None)
	_window = ObjectProperty(None, allownone=True)
	status = False #是否打开
	child_menu = None #打开的子菜单
	parent_menu = None #父菜单

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

	def open(self, pos, open_type='click', size=(0, 0)):
		if self.status: return

		if self._window is not None:
			Logger.warning('ModalView: you can only open once.')
			return self
		# search window
		self._window = self._search_window()
		if not self._window:
			Logger.warning('ModalView: cannot open view, no window found.')
			return self

		x, y = pos
		if open_type == 'click':
			if self.width + x > self._window.width:
				x = self._window.width - self.width

			if y > self.height:
				y -= self.height

		elif open_type == 'enter':
			width, height = size
			if self.width + x + width > self._window.width:
				x -= width - 3
			else:
				x += width - 3

			if y > self.height:
				y = y - self.height + height

		self.pos = (x, y)
		#Logger.info(str(self.pos))
		self._window.add_widget(self)

		self.status = True
		if self.parent_menu:
			self.parent_menu.child_menu = self
		return self

	def close(self):
		#递归关闭所有节点
		for child in self.children:
			if child.select == 1:
					child.selected(0)
			if child.click_menu:
				child.click_menu.close()

		if self._window is None:
			return self
		self._window.remove_widget(self)
		self._window = None
		self.status = False
		#关闭时父控件的child_menu置空
		if self.parent_menu:
			self.parent_menu.child_menu = None
		return self
