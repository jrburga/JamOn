from game import GameObject
from kivy.core.window import Window
from components.sprites import GemSprite, LaneSprite, TrackSprite, NowBarSprite

class Track(GameObject):
	def __init__(self, num_lanes, bars, tempo):
		super(Track, self).__init__()
		self.lanes = [Lane() for i in range(num_lanes)]
		self.now = 0
		self.sprite = TrackSprite()
		self.now_bar = NowBarSprite()
		w, h = self.sprite.size

		div = w/num_lanes
		self.position = ((Window.width-w)/2, 0)

		for i, lane in self.lanes:

		self.tempo = tempo
		self.bars = bars

		# self.t2y_ratio = 

		self.add_graphic(self.sprite)
		self.add(*self.lanes)
		self.add_graphic(self.now_bar)

	# def time2y(self, time):

		
	def on_press(self, lane_num):
		self.lanes[lane_num].on_press(self.now)

	def on_release(self, lane_num):
		self.lanes[lane_num].on_release(self.now)

	def on_update(self):
		x, _ = self.now_bar.position
		y = self.now
		self.now_bar.position = (x, y)


class Lane(GameObject):
	def __init__(self):
		super(Lane, self).__init__()
		self.sprite = LaneSprite()
		self.gems = []
		w, h = self.sprite.size
		for gem in self.gems:
			gem.sprite.size = (w, h)
		self.add(*self.gems)
		self.add_graphic(self.sprite)

	@property
	def track(self):
		return self._parent

	def on_hit(self):
		pass

	def on_pass(self):
		pass

	def on_press(self, time):
		pass

	def on_release(self, time):
		pass

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
