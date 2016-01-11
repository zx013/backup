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
	signal('clickmenu_init', self)
	signal('filelist_init', self)
	signal('titlelabel_init', self)
	signal('statusbar_init', self)
	signal('operatelist_init', self)
connect('system_init', system_init)