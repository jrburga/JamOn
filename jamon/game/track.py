from game import GameObject
from kivy.core.window import Window
from components.sprites import GemSprite, LaneSprite, TrackSprite

class Track(GameObject):
	def __init__(self, num_lanes):
		super(Track, self).__init__()
		self.lanes = [Lane() for i in range(num_lanes)]
		self.sprite = TrackSprite()
		w, h = self.sprite.size
		self.position = ((Window.width-w)/2, 0)
		self.add_graphic(self.sprite)
		self.add(*self.lanes)

	def on_press(self, lane_num):
		self.lanes[lane_num].on_press()

	def on_release(self, lane_num):
		self.lanes[lane_num].on_release()


class Lane(GameObject):
	def __init__(self):
		super(Lane, self).__init__()
		self.sprite = LaneSprite()
		self.gems = []
		self.add(*self.gems)
		self.add_graphic(self.sprite)

	@property
	def track(self):
		return self._parent

	def on_hit(self):
		pass

	def on_pass(self):
		pass

	def on_press(self):
		pass

	def on_release(self):
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
