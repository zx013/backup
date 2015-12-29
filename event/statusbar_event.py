#-*- coding:utf-8 -*-

#更新方式
#定时刷新 备份介质信息
#函数起止 备份状态信息

global num
num = 1

def status_1(self):
	global num
	self.text = str(num)
	num += 1

def status_2(self):
	pass

def status_3(self):
	pass

def status_4(self):
	pass


statusbar_mark = [None, None, 3, 4] #None为定时刷新
statusbar_event = [status_1, status_2, status_3, status_4]