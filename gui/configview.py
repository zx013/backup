#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.popup import Popup

from kivy.lang import Builder
Builder.load_file('gui/configview.kv')


class ConfigView(Popup):
	pass