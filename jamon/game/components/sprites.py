from graphics import *
from kivy.core.window import Window

gem_texture = Rectangle()
track_width = Window.width*.4
lane_width = track_width
now_bar_width = 5
track_size = (track_width, Window.height-10)
lane_size = (lane_width, Window.height-10)
now_bar_size = (track_width, now_bar_width)
gem_size = (lane_width, now_bar_width)
bar_line_size = (track_width, 2)

player_size = (track_width+10, Window.height-10)

pattern_list_height = Window.height
pattern_list_size=(Window.width - track_width-35, pattern_list_height)
pattern_height = 50
pattern_size = (pattern_list_size[0] - 10, pattern_height)
pattern_now_bar_size = (3, pattern_height)

lane_line_size = (7, track_size[1])

inst_panel_size = (pattern_list_size[0], 100)


track_color = (.85, .85, .85)
now_bar_color = (.13, .54, .13)
lane_color = (.3, .3, .3)
pattern_now_bar_color = (.6, .3, .5)
# gem_texture = Image('path/to/image.png').texture

class GemSprite(RectSprite):
	def __init__(self, color):
		super(GemSprite, self).__init__(gem_size, color)

class GradientGemSprite(GradientRectSprite):
	def __init__(self, size, color_1, color_2):
		super(GradientGemSprite, self).__init__( (int(size[0]),int(size[1])), color_1, color_2, dir='vertical')

class TrackSprite(RectOutlineSprite):
	def __init__(self):
		super(TrackSprite, self).__init__(track_size, track_color)
		# self.center = (Window.width/2, Window.height/2)

class LaneSprite(RectOutlineSprite):
	def __init__(self):
		super(LaneSprite, self).__init__(lane_size, lane_color)

class NowBarSprite(RectSprite):
	def __init__(self):
		super(NowBarSprite, self).__init__(now_bar_size, now_bar_color)

class BarLineSprite(RectSprite):
	def __init__(self, ind):
		color = (1,1,1) if ind % 4 == 0 else (.5, .5, .5)
		super(BarLineSprite, self).__init__(bar_line_size, color)
class LaneLineSprite(RectSprite):
	def __init__(self):
		color = (.5, .5, .5)
		super(LaneLineSprite, self).__init__(lane_line_size, color)

class PlayerOutlineSprite(RectOutlineSprite):
	def __init__(self, me):
		color = (.3, .6, .3) if me else (.4, .4, .4)
		super(PlayerOutlineSprite, self).__init__(player_size, color)

class PatternListSprite(RectOutlineSprite):
	def __init__(self):
		color = (66./255, 220./255, 86./255)
		super(PatternListSprite, self).__init__(pattern_list_size, color)

class PatternOutlineSprite(RectOutlineSprite):
	def __init__(self):
		color = (.4,.7,1)
		super(PatternOutlineSprite, self).__init__(pattern_size, color, width=1)

class PatternNoteSprite(RectSprite):
	def __init__(self, size):
		color = (0.4, 1, 0.7)
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
		super(InstrumentPanelSrite, self).__init__(inst_panel_size, (0,0,0))




