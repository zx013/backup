#-*- coding:utf-8 -*-
import os
from backup.config import Config
from event import connect


def get_filelist():
	config = Config()
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
	self.filelist.update(width=[w] * len(self.filelist.children))
connect('filelist_init', filelist_init)
