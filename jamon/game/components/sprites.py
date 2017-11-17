from graphics import *
from kivy.core.window import Window

gem_texture = Ellipse()
track_width = 500
lane_width = 50
now_bar_width = 10
track_size = (track_width, Window.height)
lane_size = (lane_width, Window.height)
now_bar_size = (track_width, now_bar_width)

track_color = (.85, .85, .85)
now_bar_color = (0, 0, 0)
lane_color = (1, 1, 1)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(Sprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_texture, color)

class TrackSprite(RectSprite):
	def __init__(self):
		super(TrackSprite, self).__init__(track_size, track_color)
		# self.center = (Window.width/2, Window.height/2)

class LaneSprite(RectSprite):
	def __init__(self):
		super(LaneSprite, self).__init__(lane_size, lane_color)

class NowBarSprite(RectSprite):
	def __init__(self):
		super(NowBarSprite, self).__init__(now_bar_size, now_bar_color)

