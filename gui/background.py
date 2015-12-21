#-*- coding:utf-8 -*-
from kivy.properties import ListProperty

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