#-*- coding:utf-8 -*-
from event import connect


def get_titlelabel():
	return ['名称', '修改日期', '设备', '大小']


def titlelabel_init(*args, **kwargs):
	self = args[0]
	w = [180, 180, 60, 40]
	self.titlelabel.insert(text=get_titlelabel())
	self.titlelabel.update(width=w)
	self.titlelabel.auto_sort() #自动排序
connect('titlelabel_init', titlelabel_init)
