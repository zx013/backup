#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App

from filemanager import FileManager

class DisplayScreen(FileManager):
	def build(self):
		self.filelist.insert(a=[range(4)] * 32)
		t = []
		for i in range(len(self.filelist.children)):
			t.append(['a%s' % i, 'b', 'c', 'd', 'ab'])
		self.filelist.update(text=t)
		self.filelist.update(width=[[120, 80, 160, 40]] * len(self.filelist.children))
		#f.delete(text=[[('a', 'b'), ('a', 'c'), 'd', 'e']] * len(self.filelist.children))

		self.titlelabel.insert(text=['title-0', 'title-1', 'title-2', 'title-3'])
		self.titlelabel.update(width=[120, 80, 160, 40])

		self.filelist.click_menu.insert(text=['a', ['b', 'b1', 'b2', 'b3', 'b4', 'b5', ['ee', 'ee1', 'ee2', ['f', 'f1', ['g', ['h', 'h1']]]]], ['c', 'c1', 'c2'], 'd'])


class mainApp(App):
	def build(self):
		ds = DisplayScreen()
		ds.build()
		return ds

if __name__ == '__main__':
	mainApp().run()
