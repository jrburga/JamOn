from graphics import *
from kivy.core.window import Window

gem_texture = Ellipse()
track_width = 100
now_bar_width = 10
track_size = (track_width, Window.height)
now_bar_size = (track_width, now_bar_width)

track_color = (.75, .75, .75)
now_bar_color = (0, 0, 0)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(Sprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_texture, color)

	def on_update(self, dt):
		return super(GemSprite, self).on_update(dt) and !self.dead

	def kill(self):
		self.dead = True

class TrackSprite(RectSprite):
	def __init__(self):
		super(TrackSprite, self).__init__(track_size, track_color)

class NowBarSprite(RectSprite):
	def __init__(self):
		super(NowBarSprite, self).__init__(now_bar_size, now_bar_color)

