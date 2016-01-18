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

from kivy.lang import Builder
Builder.load_file('gui/file_list.kv')

title = ['name', 'time']

def get_data(name):
	data = {'name': name[0], 'data': name[1], 'time': name[2]}
	return data

data = {}
for i in range(10):
	name = '%dbc' % i
	data[name] = get_data(name)


class FileLabel(ListItemLabel):
	selected_color = ListProperty([1., 0., 0., 1])
	above_color = ListProperty([0., 0., 1., 1])
	deselected_color = ListProperty([0., 1., 0., 1])
	
	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				self.select()
		super(FileLabel, self).on_touch_down(touch)	


#传入title和func，func根据名称获取title对应的信息
class File_List(ListView):
	data = ''
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
				cls_dicts.append({'cls': FileLabel, 'kwargs': {'text': str(rec.get(i))}})
			ret['cls_dicts'] = cls_dicts
			return ret
		dict_adapter = DictAdapter(
			sorted_keys=sorted(data.keys(), key=lambda x: data[x].get(self.key), reverse=self.reverse),
			data=data,
			args_converter=args_converter,
			selection_mode='multiple',
			allow_empty_selection=False,
			cls=CompositeListItem)
		self.adapter = dict_adapter
		self.data = self.adapter.data
		self.size_hint = (.2, 1.0)

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
				self.insert('cde')
				self.sort(key='name') #排序变化后清空选中项
			elif touch.button == 'right':
				self.delete('cde')
		super(File_List, self).on_touch_down(touch)


class mainApp(App):
	def build(self):
		listview = File_List(title=title, converter=get_data)
		return listview

if __name__ == '__main__':
	mainApp().run()