import traceback
from kivy.app import App

from jamon.main import widget

class MainApp(App):
	def build(self):
		return widget()

if __name__ == '__main__':
	MainApp().run()






