from game import GameObject
from player import Player
from kivy.clock import Clock as kivyClock


# default music settings
tempo = 120
bars = 4
divs = 4

class Session(GameObject):
	def __init__(self):
		super(Session, self).__init__()
		self.tempo = tempo
		self.bars = bars
		self.divs = divs
		self.time = 0
		self.players = [Player(bars, tempo)]
		self.player_index = 0

		self.add(*self.players)

	def on_update(self):
		for player in self.players:
			player.set_now(kivyClock.time())