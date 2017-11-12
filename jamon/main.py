from common.core import BaseWidget
from common.audio import Audio

from scene import Scene

class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()
		self.audio = Audio(2)
		self.scene = Scene()

		self.audio.set_generator(self.scene.mixer)
		self.canvas.add(self.scene.graphics)
		
	def on_key_down(self, keycode, modifiers):
		self.scene.trigger_event('on_key_down', 
								  keycode=keycode, 
								  modifiers=modifiers)

	def on_key_up(self, keycode):
		self.scene.trigger_event('on_key_up',
								 keycode=keycode)
		
	def on_touch_down(self, touch):
		self.scene.trigger_event('on_touch_down',
								  touch=touch)

	def on_touch_up(self, touch):
		self.scene.trigger_event('on_touch_up',
								  touch=touch)

	def on_touch_move(self, touch):
		self.scene.trigger_event('on_touch_move',
								  touch=touch)

	def on_update(self):
		self.scene.on_update()
		self.audio.on_update()


if __name__ == '__main__':
	pass