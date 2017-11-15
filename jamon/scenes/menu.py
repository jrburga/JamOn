
from ..game import Scene, GameObject
from ..components.graphics import *
# from kivy.graphics import Ellipse
from ..common.gfxutil import CEllipse, Color

from ..objects.controller import Keyboard

scene = Scene()

def print_event(scene, event):
	print 'event was triggered'
	print scene, event.keycode

def on_click(go, event):
	print go, event

def check_button(button, event):
	print button.graphic.shape.pos
	print button.graphic.shape.size
	button.on_click(event)

class Button(GameObject):
	def __init__(self, graphic):
		super(Button, self).__init__()
		self.graphic = graphic
		self.add_event_listener('on_touch_down', check_button)
		self.add_graphic(self.graphic)

	def on_click(self, event):
		print event.touch.pos

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

# button = Button(CircleGraphic(100, (1, 1, 1)))

circle.position = (100, 100)
scene.add_game_object(circle)
scene.add_game_object(Keyboard())
# scene.add_game_object(button)
