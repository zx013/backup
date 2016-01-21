#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.logger import Logger
from kivy.uix.modalview import ModalView

from kivy.lang import Builder
Builder.load_file('gui/configview.kv')


class ConfigView(ModalView):
	def get_ignore(self, spinner, ignore):
		#Logger.info(str(ignore))
		self.ignore.clear()
		if ignore:
			self.ignore.insert(text=map(lambda x: [x], ignore))