from game import GameObject
from components.sprites import GemSprite, LaneSprite, TrackSprite, NowBarSprite

# Should really fix this graphically and not here.
OFFSET = 7

class Track(GameObject):
	def __init__(self, num_lanes, bars, tempo):
		super(Track, self).__init__()
		self.lanes = [Lane() for i in range(num_lanes)]
		self.now = 0
		self.sprite = TrackSprite()
		self.now_bar = NowBarSprite()
		self.w, self.h = self.sprite.size
		# w, h = self.sprite.size

		spb = 60./tempo
		beats = bars*4
		self.seconds = spb*beats

		self.t2y = self.h/self.seconds
		# self.scale.x = 0.5
		# self.position = ((Window.width-self.w)/2, 0)

		i2lane = self.w/num_lanes
		for i, lane in enumerate(self.lanes):
			lane.position.x = i*i2lane+OFFSET

		self.tempo = tempo
		self.bars = bars

		# self.t2y_ratio = 

		self.add_graphic(self.sprite)
		self.add(*self.lanes)
		self.add_graphic(self.now_bar)

	def t2y_conversion(self, time):
		return self.sprite.height-self.t2y

	# def time2y(self, time):
	def on_press(self, lane_num):
		self.lanes[lane_num].on_press(self.now)

	def on_release(self, lane_num):
		self.lanes[lane_num].on_release(self.now)

	def on_update(self):
		x, _ = self.now_bar.position
		y = self.h-self.t2y*(self.now%self.seconds)
		self.now_bar.position = (x, y)


class Lane(GameObject):
	def __init__(self):
		super(Lane, self).__init__()
		self.sprite = LaneSprite()
		cx, cy = self.sprite.center
		# self.sprite.center = (cx)
		self.gems = [] 
		# kind of redundant since all game_objets
		# owned by a lane will be gems
		# but maybe not since _game_objects is a set()
		w, h = self.sprite.size
		self.add_graphic(self.sprite)

	# @property
	# def gems(self):
	# 	return self._game_objects

	@property
	def track(self):
		return self._parent

	def on_hit(self):
		pass

	def on_pass(self):
		pass

	def on_press(self, time):
		self.sprite.color.rgb = (1, 0, 0)
		gem = Gem((1, 0, 0))
		self.add(gem)

	def on_release(self, time):
		self.sprite.color.rgb = (1, 1, 1)

class Gem(GameObject):
	def __init__(self, color, time=0, length=0):
		super(Gem, self).__init__()
		self.sprite = GemSprite(color)
		self.add_graphic(self.sprite)

	@property
	def lane(self):
		return self._parent

	def on_hit(self, *args):
		pass

	def on_miss(self, *args):
		pass
