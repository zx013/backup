#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.gridlayout import GridLayout
from titlelabel import TitleLabel
from filelist import FileList
from statusbar import StatusBar
from operatelist import OperateList

from kivy.lang import Builder
Builder.load_file('gui/mainview.kv')
Builder.load_file('gui/filemanager.kv')

class MainView(GridLayout):
	pass