#-*- coding:utf-8 -*-
from implevent import connect
from gui.clickmenu import ClickMenu


def clickmenu_1(*args, **kwargs):
	pass

def clickmenu_2(*args, **kwargs):
	pass

def clickmenu_3(*args, **kwargs):
	pass

def clickmenu_4(*args, **kwargs):
	pass

def clickmenu_5(*args, **kwargs):
	pass


clickmenu_text = ['立即备份', '恢复文件', '恢复到最近的备份', '管理备份', '删除备份']
clickmenu_event = [clickmenu_1, clickmenu_2, clickmenu_3, clickmenu_4, clickmenu_5]

def clickmenu_init(*args, **kwargs):
	self = args[0]
	self.filelist.click_menu = ClickMenu()
	self.filelist.click_menu.insert(text=clickmenu_text, event=clickmenu_event)
connect('clickmenu_init', clickmenu_init)