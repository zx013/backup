#-*- coding:utf-8 -*-
import os
from backup.config import Config
from implevent import connect

global config
config = Config()

def get_filelist():
	global config
	config.read_config()
	filelist = config.config['backup'].keys()

	t = []
	for f in filelist:
		if os.path.exists(f):
			f_stat= os.stat(f)
			t.append(map(str, [f.encode('utf-8'), f_stat.st_mtime, f_stat.st_dev, f_stat.st_size]))
	return t


def filelist_init(*args, **kwargs):
	self = args[0]
	w = [180, 180, 60, 40]
	#self.filelist.destroy()
	self.filelist.insert(text=get_filelist())
	self.filelist.insert(text=get_filelist())
	self.filelist.update(width=[w] * len(self.filelist.children))
	#用None填充无须比较的字段，列表最后的None通配后面所有值
	self.filelist.delete(text=[['C:/Users//Administrator/Desktop/a.doc', None]])
	#self.filelist.clear()
connect('filelist_init', filelist_init)
