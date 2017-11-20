from game import GameObject

from controller import Keyboard
from instrument import Instrument
from track import Track

num_lanes = 8
default_keys = [
	['a', 's', 'd', 'f', 'q', 'w', 'e', 'r'], 
	['j', 'k', 'l', ';', 'u', 'i', 'o', 'p']
]

# assert([len(dk) == num_lanes for dk in default_keys])

default_keys = [[ord(k) for k in dk] for dk in default_keys]

class Player(Keyboard):
	def __init__(self, bars, tempo, num=0, inst='piano'):
		super(Player, self).__init__()
		self.keys = default_keys[num]
		self.instrument = Instrument(inst)

		self.track = Track(num_lanes, bars, tempo)

		self.add(self.track)

	def key_down(self, lane_num):
		self.track.on_press(lane_num)
		self.instrument.note_on(lane_num)

	def key_up(self, lane_num):
		self.track.on_release(lane_num)
		self.instrument.note_off(lane_num)

	def set_now(self, time):
		self.track.now = time

	def on_update(self):
		pass

	@property
	def session(self):
		return self._parent

	def lock_in(self):
		pass

