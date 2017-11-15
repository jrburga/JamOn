from graphics import *
from kivy.core.window import Window

gem_texture = Ellipse()
track_size = (100, Window.height)
track_color = (.75, .75, .75)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(Sprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_texture, color)

class TrackSprite(RectSprite):
	def __init__(self):
		super(TrackSprite, self).__init__(track_size, track_color)

