from graphics import *
from jamon.game.window import Window
from kivy.graphics import Color

gem_texture = Rectangle()
track_width = Window.width * .35
lane_width = track_width
now_bar_width = 5
track_size = (track_width, Window.height * 0.9)
lane_size = (lane_width, Window.height * 0.9)
now_bar_size = (track_width, now_bar_width)
gem_size = (lane_width, now_bar_width)
bar_line_size = (track_width, 3)
downbeat_bar_line_size = (track_width, 5)

player_size = (track_width+10, Window.height-10)

pattern_list_height = Window.height
pattern_list_size=(Window.width - track_width-35, pattern_list_height)
pattern_height = Window.height * 0.1
pattern_size = (pattern_list_size[0] - 10, pattern_height)
pattern_now_bar_size = (3, pattern_height)

lane_line_size = (7, track_size[1])

inst_panel_size = (pattern_list_size[0], Window.height * 0.1)
volume_slider_size = (pattern_size[0]*0.1, 20)



track_color = DARK_GRAY
now_bar_color = (.13, .54, .13)
lane_color = (.9, .9, .9)
dark_lane_color = (0.85, 0.85, 0.85)
pattern_now_bar_color = (.6, .3, .5)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(RectSprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_size, color)

class GradientGemSprite(ImageSprite):
	def __init__(self, size, color_1, color_2):
		super(GradientGemSprite, self).__init__('gradient.png', color_2, size=size)
		# super(GradientGemSprite, self).__init__( (int(size[0]),int(size[1])), color_1, color_2, dir='vertical')

class TrackSprite(RectOutlineSprite):
	def __init__(self):
		super(TrackSprite, self).__init__(track_size, track_color, width=4)
		# self.center = (Window.width/2, Window.height/2)

class LaneSprite(RectSprite):
	def __init__(self, ind):
		color = lane_color if ((ind % 2) == 0) else dark_lane_color
		super(LaneSprite, self).__init__(lane_size, color)

class NowBarSprite(RectSprite):
	def __init__(self):
		super(NowBarSprite, self).__init__(now_bar_size, now_bar_color)

class BarLineSprite(RectSprite):
	def __init__(self, ind):
		color = DARKER_GRAY
		size = bar_line_size if ((ind % 4) != 0) else downbeat_bar_line_size
		super(BarLineSprite, self).__init__(size, color)

class LaneLineSprite(RectSprite):
	def __init__(self):
		color = DARKER_GRAY
		super(LaneLineSprite, self).__init__(lane_line_size, color)

class PlayerOutlineSprite(RectOutlineSprite):
	def __init__(self, me):
		color = (.3, .6, .3) if me else (.4, .4, .4)
		super(PlayerOutlineSprite, self).__init__(player_size, color)

class PatternListSprite(RectOutlineSprite):
	def __init__(self):
		color = (66./255, 220./255, 86./255)
		super(PatternListSprite, self).__init__(pattern_list_size, color)

class PatternOutlineSprite(RectSprite):
	def __init__(self):
		color = YELLOW
		super(PatternOutlineSprite, self).__init__(pattern_size, color)

class PatternNoteSprite(RectSprite):
	def __init__(self, size):
		color = invert_color(BLUE)
		super(PatternNoteSprite, self).__init__(size, color)

class PatternPlaySprite(ImageSprite):
	def __init__(self):
		color = (0, .6, .8)
		size = (30,30)
		super(PatternPlaySprite, self).__init__('play.png', color, size=size)

class PatternDeleteSprite(ImageSprite):
	def __init__(self):
		color = (1, .3, 0)
		size = (30,30)
		super(PatternDeleteSprite, self).__init__('delete.png', color, size=size)

class PatternInstrumentIconSprite(ImageSprite):
	def __init__(self, fname):
		size = (30,30)
		color = (73./255, 155./255, 132./255)
		super(PatternInstrumentIconSprite, self).__init__(fname, size=size, color=color)

class PatternAddSprite(ImageSprite):
	def __init__(self):
		size = (30,30)
		super(PatternAddSprite, self).__init__('add.png', size=size)

class PatternNowBarSprite(RectSprite):
	def __init__(self):
		super(PatternNowBarSprite, self).__init__(pattern_now_bar_size, pattern_now_bar_color)

class PatternInstrumentSprite(ImageSprite):
	def __init__(self, fname):
		size = (48,48)
		super(PatternInstrumentSprite, self).__init__(fname, size=size)

class InstrumentPanelSrite(RectSprite):
	def __init__(self):
		super(InstrumentPanelSrite, self).__init__(inst_panel_size, GRAY)

class VolumeOutlineSprite(RectOutlineSprite):
	def __init__(self):
		color = Color(0,.6,1, mode='hsv').rgb
		super(VolumeOutlineSprite, self).__init__(volume_slider_size, color, width=1)

class VolumeInsideSprite(RectSprite):
	def __init__(self, volume):
		color =  Color(0,.8,1, mode='hsv').rgb
		w, h = volume_slider_size
		w -= 10
		w = int(w * volume)
		h -= 10
		super(VolumeInsideSprite, self).__init__((w,h), color)

	def set_volume(self, volume):
		w, h = volume_slider_size
		w -= 10
		w = int(w * volume)
		h -= 10
		self.texture.size = (w, h)





