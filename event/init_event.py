#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #Ìí¼Óµ½ËÑË÷Â·¾¶

from event import signal, connect
import clickmenu_event
import filelist_event
import titlelabel_event
import statusbar_event
import operatelist_event


def system_init(*args, **kwargs):
	self = args[0]
	signal('clickmenu_init', self.ids['d_filemanager'])
	signal('filelist_init', self.ids['d_filemanager'])
	signal('titlelabel_init', self.ids['d_filemanager'])
	signal('statusbar_init', self.ids['d_statusbar'])
	signal('operatelist_init', self.ids['d_operatelist'])
connect('system_init', system_init)