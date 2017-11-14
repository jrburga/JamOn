import sys
sys.path.append('..')

from game import Scene, GameObject
from graphics.graphic import *
# from kivy.graphics import Ellipse
from common.gfxutil import CEllipse, Color

scene = Scene()

def print_event(scene, event):
	print 'event was triggered'
	print scene, event

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

scene.add_event_listener('on_key_down', print_event)

circle = GameObject()
circle.position = (100, 100)
circle.rotation = 90
circle.add_graphic(CircleGraphic(100, (1, 1, 1)))

circle2 = GameObject()
circle2.scale = 0.5
circle2.add_graphic(Color(rgb=(1, 0, 0)))
circle2.add_graphic(CEllipse())

circle3 = GameObject()
circle3.scale = 0.5
circle3.add_graphic(Color(rgb=(0, 1, 0)))
circle3.add_graphic(CEllipse())


circle.add_game_object(circle2)
circle2.add_game_object(circle3)

button = Button(CircleGraphic(100, (1, 1, 1)))


scene.add_game_object(circle)
scene.add_game_object(button)
