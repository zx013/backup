#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')
import sys
sys.path.append('.')

from kivy.app import App

from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemLabel, ListItemButton, CompositeListItem, ListView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

from kivy.logger import Logger

from kivy.lang import Builder
Builder.load_file('gui/file_list.kv')

title = ['name', 'time']

def get_data(name):
	data = {'name': name, 'data': name[0], 'time': name[2]}
	return data

data = {}
for i in range(10):
	name = '%dbc' % i
	data[name] = get_data(name)


class FileItem(ListItemLabel):
	pass

global a
a = 0

class FileLabel(CompositeListItem):
	selected_space_color = ListProperty([0, .6, 1, .3])
	selected_frame_color = ListProperty([0, .6, 1, .6])
	above_space_color = ListProperty([0, .6, 1, .1])
	above_frame_color = ListProperty([0, .6, 1, .4])
	deselected_space_color = ListProperty([0, .6, 1, 0])
	deselected_frame_color = ListProperty([0, .6, 1, 0])
	
	background_space_color = ListProperty([0, .6, 1, 0])
	background_frame_color = ListProperty([0, .6, 1, 0])

	def __init__(self, **kwargs):
		super(FileLabel, self).__init__(**kwargs)
		global a
		self.a = a
		a += 1
		Logger.warning('init, %d' % self.a)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				pass
				#if self.is_selected:
				#	self.deselect()
				#else:
				#	self.select()
				#Logger.warning(str(map(lambda x: x.is_selected, self.parent.children)))
		super(FileLabel, self).on_touch_down(touch)

	def select(self, *args):
		Logger.warning('select, %d' % self.a)
		self.is_selected = True
		self.background_space_color = self.selected_space_color
		self.background_frame_color = self.selected_frame_color
		for c in self.children:
			c.select_from_composite(*args)

	def deselect(self, *args):
		Logger.warning('deselect, %d' % self.a)
		self.is_selected = False
		self.background_space_color = self.deselected_space_color
		self.background_frame_color = self.deselected_frame_color
		for c in self.children:
			c.deselect_from_composite(*args)


#传入title和func，func根据名称获取title对应的信息
class File_List(ListView):
	container_x = 0
	container_y = 0

	data = {}
	#排序的类型
	key = 'name'
	#排序的方向
	reverse = True
	def __init__(self, **kwargs):
		super(File_List, self).__init__(**kwargs)
		self.title = kwargs['title']
		self.converter = kwargs['converter']
		def args_converter(row_index, rec):
			ret = {'size_hint_y': None, 'height': 25}
			cls_dicts = []
			for i in self.title:
				cls_dicts.append({'cls': FileItem, 'kwargs': {'text': str(rec.get(i))}})
			ret['cls_dicts'] = cls_dicts
			return ret
		dict_adapter = DictAdapter(
			sorted_keys=sorted(data.keys(), key=lambda x: data[x].get(self.key), reverse=self.reverse),
			data=data,
			args_converter=args_converter,
			selection_mode='multiple',
			allow_empty_selection=True,
			cls=FileLabel)
		self.adapter = dict_adapter
		self.data = self.adapter.data

	#计算文件列表所在的坐标
	def container_pos(self):
		self.container_x = self.x
		self.container_y = self.y + self.height - sum(map(lambda x: x.height, self.container.children))

	def insert(self, name):
		if not self.data.has_key(name):
			self.data[name] = get_data(name)

	def update(self, name):
		self.data[name] = get_data(name)

	def sort(self, key=None):
		if not len(self.data):
			return
		if key is not None and self.data.values()[0].has_key(key):
			self.key = key
			self.reverse = True
		else:
			self.reverse = not self.reverse
		self.adapter.sorted_keys = sorted(self.data.keys(), key=lambda x: self.data[x].get(self.key), reverse=self.reverse)

	def delete(self, name):
		if self.data.has_key(name):
			del self.data[name]

	def refresh(self):
		for name in self.data:
			self.data[name] = get_data(name)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				#self.insert('cde')
				self.container_pos()
				for child in self.container.children:
					if child.collide_point(touch.x - self.container_x, touch.y - self.container_y):
						self.adapter.handle_selection(child, hold_dispatch=True)
						break
				Logger.warning(str(self.adapter.selection))
			elif touch.button == 'right':
				self.sort() #排序变化后清空选中项
				Logger.warning(str(map(lambda x: x.is_selected, self.container.children)))
				selected_list = filter(lambda child: child.is_selected, self.container.children)
				Logger.warning(str(selected_list))
				self.adapter.select_list(selected_list)
				#self.adapter.select_list(selected_list)
				#self.delete('cde')
				#self.refresh()
				#self.adapter.select_list(var)
				Logger.warning(str(self.adapter.selection))

		super(File_List, self).on_touch_down(touch)


class mainApp(App):
	def build(self):
		listview = File_List(title=title, converter=get_data)
		return listview

if __name__ == '__main__':
	mainApp().run()