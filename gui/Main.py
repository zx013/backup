#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput


class MyTextInput(TextInput):
	pass

class MainWidget(Widget):
	pass

class Main(App):
    def build(self):
        return MainWidget()

if __name__ == '__main__':
	Main().run()