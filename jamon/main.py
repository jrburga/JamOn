from game.common.core import *
from game.common.audio import Audio

from scenes import scenes

class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()
		self.audio = Audio(2)

		self.scenes = {scene.name: scene for scene in scenes}
		self.scene = None
		for scene in scenes:
			if scene.is_start():
				self.set_scene(scene)
				break
		else:
			self.set_scene[scenes[0]]

	def set_scene(self, scene):
		print 'changing scene'
		if self.scene:
			print 'removing graphics'
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
		if self.scene.change_scene():
			self.set_scene(self.scenes[self.scene.next_scene()])
