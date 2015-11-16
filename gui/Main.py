#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.textinput import TextInput


class MyTextInput(TextInput):
	pass

class Main(App):
    def build(self):
        return MyTextInput()

if __name__ == '__main__':
	Main().run()