from game import GameObject
from player import Player
from kivy.clock import Clock as kivyClock
from kivy.core.window import Window


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
		self.players = [Player(bars, tempo), Player(bars, tempo, num=1)]
		i2player = Window.width/len(self.players)
		scale = 1./len(self.players)
		for i, player in enumerate(self.players):
			player.position.x = i2player*i+80
			player.scale.x = scale
			continue
		self.current_player = 0

		self.add(*self.players)

	def on_update(self):
		for player in self.players:
			player.set_now(kivyClock.time())