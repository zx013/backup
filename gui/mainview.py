#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.gridlayout import GridLayout

from kivy.lang import Builder
Builder.load_file('gui/mainview.kv')
Builder.load_file('gui/filemanager.kv')
Builder.load_file('gui/operatelist.kv')
Builder.load_file('gui/titlelabel.kv')
Builder.load_file('gui/filelist.kv')
Builder.load_file('gui/statusbar.kv')

class MainView(GridLayout):
	pass