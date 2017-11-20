from game import GameObject
from player import Player
from instrument import InstrumentManager	
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
		spb = 60./tempo
		beats = bars*4
		self.seconds = spb*beats
		self.time = 0
		self.players = [Player(bars, tempo), Player(bars, tempo, num=1)]
		self.IM = InstrumentManager()

		i2player = Window.width/len(self.players)
		scale = 1./len(self.players)
		for i, player in enumerate(self.players):
			player.position.x = i2player*i+80
			player.scale.x = scale
			self.IM.add(player.instrument)
			continue
		self.current_player = 0

		self.add(*self.players)
		self.add(self.IM)

	def on_update(self):
		for player in self.players:
			player.set_now(kivyClock.time()%self.seconds)