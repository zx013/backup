#-*- coding:utf-8 -*-

global event
event = {}

#²úÉúevent
def signal(sign, *args, **kwargs):
	global event
	for func in event.get(sign, []):
		if hasattr(func, '__call__'):
			func(*args, **kwargs)

#eventÏìÓ¦
def connect(sign, func):
	global event
	event.setdefault(sign, [])
	event[sign].append(func)
