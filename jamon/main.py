from common.core import *
from common.audio import Audio

from game import Game
from scenes import menu

class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()
		self.audio = Audio(2)

		self.scene = menu.scene
		self.set_scene(self.scene)

	def set_scene(self, scene):
		if self.scene:
			self.canvas.remove(self.scene._graphics)
		self.scene = scene
		self.audio.set_generator(scene._mixer)
		self.canvas.add(scene._graphics)

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
		self.scene._on_update()
		self.audio.on_update()