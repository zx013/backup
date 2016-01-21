#-*- coding:utf-8 -*-
from event import connect
from gui.clickmenu import ClickMenu


def clickignore_1(*args, **kwargs):
	pass

def clickignore_2(*args, **kwargs):
	pass

def clickignore_3(*args, **kwargs):
	pass


clickignore_text = ['add', 'mod', 'del']
clickignore_event = [clickignore_1, clickignore_2, clickignore_3]

def clickignore_init(*args, **kwargs):
	self = args[0]
	self.click_menu = ClickMenu()
	self.click_menu.insert(text=clickignore_text, event=clickignore_event)
connect('clickignore_init', clickignore_init)