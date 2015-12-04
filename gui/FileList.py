#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from clickmenu import BackGround, ClickMenu
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

	#side: True右侧，False左侧
	#direction: 拉伸的方向，True向右，False往左
	#value: 拉伸的值
	def stretch(self, side, direction, value):
		#Logger.info('before: %s,%s' % (str(self.pos), str(self.size)))
		if side:
			if direction:
				self.width += value
			else:
				self.width -= value
		else:
			if direction:
				self.width -= value
				self.x += value
			else:
				self.width += value
				self.x -= value
		#Logger.info('after: %s,%s' % (str(self.pos), str(self.size)))


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
		#如果打开了右键菜单，则不选中
		try:
			#DisplayScreen的click_menu
			if self.parent.parent.parent.click_menu.status:
				return
		except: pass
		#选中前，将其它选中的清空
		for child in self.parent.children:
			if child.select == 1:
				child.selected(0)
		if self.select == 0:	
			self.selected(1)

	def on_leave(self, *args):
		if self.select == 1:
			self.selected(0)


#调节宽度，改变排列顺序等功能
class TitleLabel(GridLayout):
	filelist = None

	#将标题栏和文件列表关联起来
	def mapping(self, filelist):
		self.filelist = filelist

	@apply_insert(AttributeLabel)
	def insert(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	def stretch(self, num, direction, value):
		self.children[::-1][num].stretch(True, direction, value)
		if len(self.children) > num + 1:
			self.children[::-1][num + 1].stretch(False, direction, value)

		#调节子标题后重新设置宽度
		self.width = sum([child.width for child in self.children])

		return
		if self.filelist:
			for filelabel in self.filelist.children:
				filelabel.children[::-1][num].stretch(True, direction, value)
				if len(filelabel.children) > num + 1:
					filelabel.children[::-1][num + 1].stretch(False, direction, value)
					#child.stretch(side, direction, value)
				filelabel.width = sum([child.width for child in filelabel.children])


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


class DisplayScreen(GridLayout):
	def build(self):
		f = ListLabel()
		f.insert(a=[range(4)] * 32)
		t = []
		for i in range(len(f.children)):
			t.append(['a%s' % i, 'b', 'a', 'd', 'ab'])
		f.update(text=t)
		f.update(width=[[120, 80, 160, 40]] * len(f.children))
		#f.delete(text=[[('a', 'b'), ('a', 'c'), 'd', 'e']] * len(f.children))
		#f.draw()
		f.bind(minimum_height=f.setter('height'), minimum_width=f.setter('width'))

		s = ScrollView()
		s.add_widget(f)

		t = TitleLabel()
		t.mapping(f)
		t.insert(text=['title-1', 'title-2', 'title-3', 'title-4'])
		t.update(width=[120, 80, 160, 40])
		self.add_widget(t)
		self.add_widget(s)
		t.stretch(0, False, 20)
		t.stretch(1, True, 20)
		t.stretch(2, False, 20)
		#Logger.info(str(t.size))

		self.click_menu = ClickMenu()
		self.click_menu.insert(text=['a', ['b', 'b1', 'b2', 'b3', 'b4', 'b5', ['ee', 'ee1', 'ee2', ['f', 'f1', ['g', ['h', 'h1']]]]], ['c', 'c1', 'c2'], 'd'])

	click_menu = None

	def on_touch_down(self, touch):
		#未打开菜单或不是
		if not self.click_menu.status or touch.button not in ['scrollup', 'scrolldown', 'middle']:
			super(DisplayScreen, self).on_touch_down(touch) #先调用子节点的事件更新select值
		#Logger.info(str(touch.button))
		if touch.button not in ['scrollup', 'scrolldown', 'middle']:
			self.click_menu.close()
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'right':
				self.click_menu.open(touch.pos)


class FileListApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	FileListApp().run()