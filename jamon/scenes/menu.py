from jamon.game.game import Scene, GameObject
from jamon.game.components.graphics import *

from jamon.game.controller import Keyboard

scene = Scene('menu', start=True)

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

circle2 = GameObject()
circle2.scale = 0.5
sprite = CircleSprite(100, (0, 0, 1))
sprite.center = (0, 0)
circle2.add_graphic(sprite)

circle3 = GameObject()
circle3.scale = 0.5
sprite = CircleSprite(100, (0, 1, 0))
sprite.center = (0, 0)
circle3.add_graphic(sprite)


circle.add_game_object(circle2)
circle2.add_game_object(circle3)

button = Button(RectSprite((100, 100), (1, 1, 1)))
print button.position.x

circle.position = (50, 50)
button.sprite.center = (0, 0)
# scene.add_game_object(circle)
scene.add_game_object(button)
# scene.add_game_object(Keyboard())
