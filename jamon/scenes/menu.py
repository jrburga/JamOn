
from jamon.game.game import Scene, GameObject
from jamon.game.components.graphics import *

from jamon.game.player import Player

scene = Scene('menu')

def print_event(scene, event):
	print 'event was triggered'
	print scene, event.keycode

def on_click(go, event):
	print go, event

class Button(GameObject):
	def __init__(self, sprite):
		super(Button, self).__init__()
		self.scale = 1
		self.sprite = sprite
		self.add_graphic(self.sprite)

	def on_touch_down(self, event):
		mx, my = event.touch.pos
		x, y = self.position.x, self.position.y
		w, h = self.sprite.size
		if mx >= x and mx <= x+w and my >= y and my <= y+h:
			self.on_click()

	def on_click(self):
		self.trigger_event('on_scene_change', scene_name='practice')

# scene.add_event_listener('on_key_down', print_event)

circle = GameObject()
sprite = CircleSprite(100, (1, 0, 0))
sprite.center = (0, 0)
circle.add_graphic(sprite)

inner = GameObject()
sprite = CircleSprite(50, (0, 1, 0))
sprite.center = (0, 0)
inner.add_graphic(sprite)
circle.add_game_object(inner)

circle.position = (200, 200)

button = Button(RectSprite((100, 100), (1, 1, 1)))

scene.add_game_object(circle)
scene.add_game_object(button)
