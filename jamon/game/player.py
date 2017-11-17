from game import GameObject

from controller import Keyboard
from instrument import Instrument
from track import Track

num_lanes = 8
default_keys = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']

assert(len(default_keys) == num_lanes)

default_keys = [ord(k) for k in default_keys]

class Player(Keyboard):
	def __init__(self):
		super(Player, self).__init__()
		self.keys = default_keys
		self.now = 0
		self.instrument = Instrument()
		self.track = Track(num_lanes)

		self.add(self.instrument, self.track)

	def key_down(self, lane_num):
		self.track.on_press(lane_num)
		self.instrument.note_on(lane_num)

	def key_up(self, lane_num):
		self.track.on_press(lane_num)
		self.instrument.note_off(lane_num)

	def on_update(self):
		pass

