from graphics import *
from kivy.core.window import Window

gem_texture = Rectangle()
track_width = 500
lane_width = 50
now_bar_width = 5
track_size = (track_width, Window.height)
lane_size = (lane_width, Window.height)
now_bar_size = (track_width, now_bar_width)
gem_size = (lane_width, now_bar_width)
bar_line_size = (lane_width, 2)

track_color = (.85, .85, .85)
now_bar_color = (.13, .54, .13)
lane_color = (1, 1, 1)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(RectSprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_size, color)

class GradientGemSprite(GradientRectSprite):
	def __init__(self, size, color_2):
		r, g, b = color_2
		color_1 = (r*.5, g*.5, b*.5)
		super(GradientGemSprite, self).__init__( (int(size[0]),int(size[1])), color_1, color_2, dir='vertical')

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

class BarLineSprite(RectSprite):
	def __init__(self, ind):
		color = (.5, .5, .5) if ind % 4 == 0 else track_color
		super(BarLineSprite, self).__init__(bar_line_size, color)


