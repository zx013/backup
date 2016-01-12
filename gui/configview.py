#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.uix.modalview import ModalView

from kivy.lang import Builder
Builder.load_file('gui/configview.kv')


class ConfigView(ModalView):
	pass