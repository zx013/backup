#-*- coding:utf-8 -*-
from event import connect


def operatelist_1(*args, **kwargs):
	pass

def operatelist_2(*args, **kwargs):
	pass

def operatelist_3(*args, **kwargs):
	self = args[0]
	self.parent.config_view.open()

operatelist_text = ['开启备份\n（暂停备份）', '文件恢复', '备份配置']
operatelist_event = [operatelist_1, operatelist_2, operatelist_3]


def operatelist_init(*args, **kwargs):
	self = args[0]
	self.insert(text=operatelist_text, event=operatelist_event)
connect('operatelist_init', operatelist_init)