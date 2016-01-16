#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')
import sys
sys.path.append('.')

from kivy.app import App

from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemLabel, ListItemButton, CompositeListItem, ListView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

from kivy.lang import Builder
Builder.load_file('gui/file_list.kv')

titles = {0: 'abc', 1: 'def', 2: 'ghi'}

def get_file_data(file_name):
	data = {0: file_name[0], 1: file_name[1], 2: file_name[2]}
	return data

data = {}
for i in range(10):
	data[i] = get_file_data('abc')

#传入title和func，func根据名称获取title对应的信息
class File_List(ListView):
	background_color = ListProperty([1, 1, 1, 1])

	selected_color = ListProperty([1., 0., 0., 1])
	above_color = ListProperty([0., 0., 1., 1])
	deselected_color = ListProperty([0., 1., 0., 1])
	def __init__(self, **kwargs):
		super(File_List, self).__init__(**kwargs)
		self.title = kwargs['title']
		self.converter = kwargs['converter']
		def args_converter(row_index, rec):
			ret = {'size_hint_y': None, 'height': 25}
			cls_dicts = []
			cls_dicts.append({'cls': ListItemButton, 'kwargs': {'text': str(rec[0])}})
			cls_dicts.append({'cls': ListItemLabel, 'kwargs': {'text': str(rec[1])}})
			cls_dicts.append({'cls': ListItemLabel, 'kwargs': {'text': str(rec[2])}})
			ret['cls_dicts'] = cls_dicts
			return ret
		#ListItemLabel.deselected_color = [.2, .5, .1, .4]
		CompositeListItem.deselected_color = [.2, .1, .5, 1]
		dict_adapter = DictAdapter(
			sorted_keys=sorted(data.keys(), key=lambda x: data[x][1]),
			data=data,
			args_converter=args_converter,
			selection_mode='multiple',
			allow_empty_selection=False,
			cls=CompositeListItem)
		self.adapter = dict_adapter
		self.size_hint = (.2, 1.0)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y) and touch.button == 'left':
			length = len(self.adapter.data)
			self.adapter.data[length] = get_file_data('cde')
		super(File_List, self).on_touch_down(touch)


class mainApp(App):
	def build(self):
		listview = File_List(title=3)
		return listview

if __name__ == '__main__':
	mainApp().run()