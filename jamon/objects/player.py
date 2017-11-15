from ..game import GameObject

from controller import Keyboard
from instrument import Instrument
from track import Track

class Player(GameObject):
	def __init__(self):
		super(Player, self).__init__()
		self.instrument = Instrument
		self.track = Track
		self.controller = Keyboard

	def on_update(self):
		pass
