#-*- coding:utf-8 -*-
from event import connect


#更新方式
#定时刷新 备份介质信息
#函数起止 备份状态信息

global num
num = 1

def status_1(*args, **kwargs):
	self = args[0]
	self.children[-1].text = str(num)
connect('statusbar_timer_event', status_1)

def status_2(*args, **kwargs):
	self = args[0]
	self.children[-2].text = str(num * 2)
connect('statusbar_timer_event', status_2)

def status_num(*args, **kwargs):
	global num
	num += 1
connect('statusbar_timer_event', status_num)

def status_3(*args, **kwargs):
	pass

def status_4(*args, **kwargs):
	pass


def statusbar_init(*args, **kwargs):
	w = [180, 180, 60, 40]
	self = args[0]
	self.insert(width=w)
	self.timer() #启动定时器
connect('statusbar_init', statusbar_init)
