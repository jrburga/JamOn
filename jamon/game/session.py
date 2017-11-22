from game import GameObject
from player import Player
from instrument import InstrumentManager	
from kivy.clock import Clock as kivyClock
from kivy.core.window import Window

from common.clock import Clock, Scheduler, SimpleTempoMap


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
		self.clock = Clock()
		self.temp_map = SimpleTempoMap(bpm=tempo)
		self.sched = Scheduler(self.clock, self.temp_map)
		self.players = [Player(bars, tempo), Player(bars, tempo, num=1), Player(bars, tempo, num=2, inst='drums')]
		self.IM = InstrumentManager(self.sched)

		i2player = Window.width/len(self.players)
		scale = 1./len(self.players)
		for i, player in enumerate(self.players):
			player.position.x = i2player*i+80
			player.scale.x = scale
			self.IM.add(player.instrument)
			continue
		self.current_player = 0
		self.num_players = len(self.players)

		self.add(*self.players)
		self.add(self.IM)

		self.clock.offset = self.seconds-spb
		print self.clock.offset
		# self.clock.start()
		self.IM.metro.start()
		self.paused = True

	def on_key_down(self, event):
		if event.keycode[1] == 'enter':
			self.toggle() 

	def toggle(self):
		if self.paused:
			self.paused = False
			self.start()
		else:
			self.paused = True
			self.stop()

	def stop(self):
		self.clock.stop()

	def start(self):
		self.clock.start()
		

	def next_player(self):
		self.players[self.current_player].composing = False
		self.current_player += 1
		if self.current_player < self.num_players:
			self.players[self.current_player].composing = True

	def on_lock_in(self, event):
		print 'locked in'
		self.next_player()

	def on_update(self):
		self.sched.on_update()
		for player in self.players:
			player.set_now(self.clock.get_time()%self.seconds)