from jamon.game.game import Scene, GameObject
from jamon.game.components.graphics import *

# For now, this code is useless and just kept around in case we want to use it later

def print_event(scene, event):
	print 'event was triggered'
	print scene, event.keycode

def on_click(go, event):
	print go, event

class Button(GameObject):
	def __init__(self, sprite, click_callback=None):
		super(Button, self).__init__()
		self.scale = 1
		self.sprite = sprite
		self.add_graphic(self.sprite)
		if click_callback:
			self.click_callback = click_callback
		else:
			self.click_callback = lambda event: self.trigger_event('on_scene_change', scene_name='practice')

	def on_touch_down(self, event):
		mx, my = event.touch.pos
		x, y = self.position.x, self.position.y
		w, h = self.sprite.size
		if mx >= x and mx <= x+w and my >= y and my <= y+h:
			self.on_click(event)

	def on_click(self, event):
		self.click_callback(event)