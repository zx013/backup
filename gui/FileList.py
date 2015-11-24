#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.animation import Animation
from kivy.logger import Logger

from Tools import apply_insert, apply_delete, apply_update, insert_args, delete_args


class BaseLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)

class FileLabel(GridLayout):
	@apply_insert(BaseLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

class FileList(GridLayout):
	@apply_insert(FileLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	def on_touch_down(self, touch):
		step = .1
		if touch.is_mouse_scrolling:
			if touch.button == 'scrollup':
				up = len(self.children) / 15.0
				if self.pos_hint['top'] < up:
					self.pos_hint['top'] += step
				else:
					self.pos_hint['top'] = up + step
				animation = Animation(pos=(self.x, self.y + 10))
				animation.start(self)
			elif touch.button == 'scrolldown':
				down = 1.0
				if self.pos_hint['top'] > down:
					self.pos_hint['top'] -= step
				else:
					self.pos_hint['top'] = down - step
				animation = Animation(pos=(self.x, self.y - 10))
				animation.start(self)


class FileListApp(App):
	def build(self):
		f = FileList()
		f.insert(a=[range(4)] * 23)
		f.update(text=[['a', 'b', 'a', 'd', 'ab']] * len(f.children))
		f.update(size_hint_x=[[.2, .3, .1, .4]] * len(f.children))
		#f.delete(text=[[('a', 'b'), ('a', 'c'), 'd', 'e']] * len(f.children))
		return f

if __name__ == '__main__':
	FileListApp().run()