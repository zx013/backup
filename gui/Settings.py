from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar


class SettingsApp(App):

	settings_cls = SettingsWithSidebar
	display_type = 'popup'
	popup = None
	
	def build(self):
		bt = Button(text='Open settings')
		bt.bind(on_press=self.open_settings)

		return bt
	
	def on_settings_cls(self, *args):
		self.destroy_settings()
	
	
	def display_settings(self, settings):
		if self.display_type == 'popup':
			if self.popup is None:
				self.popup = Popup(content=settings, title='Settings', size_hint=(0.8, 0.8))
			self.popup.open()
		else:
			super(SettingsApp, self).display_settings(settings)
	
	def close_settings(self, *args):
		if self.display_type == 'popup':
			if self.popup is not None:
				self.popup.dismiss()
		else:
			super(SettingsApp, self).close_settings()

if __name__ == '__main__':
	SettingsApp().run()
