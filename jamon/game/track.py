from game import GameObject
from components.sprites import GemSprite, LaneSprite

class Track(GameObject):
	def __init__(self):
		super(Track, self).__init__()
		self.now = 0
		self.lanes = set()

	@property
	def gems(self):
		gems = set()
		for lane in self.lanes:
			gems.add(lane.gems)
		return gems

class Lane(GameObject):
	def __init__(self):
		super(Lane, self).__init__()
		self.lane_sprite = LaneSprite()
		self.gems = set()

class Gem(GameObject):
	def __init__(self, color, time=0, length=0):
		super(Gem, self).__init__()
		self.gem_sprite = GemSprite(color)
		self.add_graphic(self.gem_sprite)
