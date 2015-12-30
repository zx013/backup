#-*- coding:utf-8 -*-
from event import connect

def click_1(*args, **kwargs):
	pass
connect('backup_event', click_1)

def click_2(*args, **kwargs):
	pass

def click_3(*args, **kwargs):
	pass

def click_4(*args, **kwargs):
	pass

def click_5(*args, **kwargs):
	pass


clickmenu_text = ['立即备份', '恢复文件', '恢复到最近的备份', '管理备份', '删除备份']
clickmenu_event = [click_1, click_2, click_3, click_4, click_5]