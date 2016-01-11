#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from clickmenu import ClickMenu
from titlelabel import TitleLabel
from filelist import FileList
from statusbar import StatusBar
from operatelist import OperateList

from tools import *

from kivy.lang import Builder
Builder.load_file('gui/filemanager.kv')


class FileManager(GridLayout):
	def __init__(self, **kwargs):
		super(FileManager, self).__init__(**kwargs)
		#文件列表
		self.filelist = FileList()
		self.filelist.click_menu = ClickMenu()
		self.filelist.bind(minimum_height=self.filelist.setter('height'), minimum_width=self.filelist.setter('width'))

		#标题栏
		self.titlelabel = TitleLabel()
		self.titlelabel.mapping(self.filelist)

		#滚动条
		self.scrollview = ScrollView()
		self.scrollview.add_widget(self.filelist)

		#状态栏
		self.statusbar = StatusBar()

		#操作按钮
		self.operatelist = OperateList()

		self.add_widget(self.operatelist)
		self.add_widget(self.titlelabel)
		self.add_widget(self.scrollview)
		self.add_widget(self.statusbar)

