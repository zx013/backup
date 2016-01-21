#-*- coding:utf-8 -*-
from backup.config import Config
from implevent import connect

global config
config = Config()

def read_config():
	global config
	config.read_config()

def configview_init(*args, **kwargs):
	pass

connect('configview_init', configview_init)