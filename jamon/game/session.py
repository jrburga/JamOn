from game import GameObject
from player import Player
from instrument import InstrumentManager
from pattern import PatternList	
from kivy.clock import Clock as kivyClock
from kivy.core.window import Window
from components.sprites import *

from common.clock import Clock, Scheduler, SimpleTempoMap

class Session(GameObject):
	def __init__(self, tempo, bars, divs):
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
		# self.players = players
		self.IM = InstrumentManager(self.sched)

		### NEW CODE ###
		self.pattern_list = PatternList(self.bars, tempo)
		self.add(self.pattern_list)
		self.player = Player(bars, tempo, inst='piano')
		self.player.position.x = Window.width - player_size[0] - 20
		self.add(self.player)
		self.IM.add(self.player.instrument)

		########## FOR TESTING ##########
		test_seq = [(0,0,1), (1,1,2), (2,1,2), (5, 3, 2), (7, 2, 5), (7,0,8)]
		self.pattern_list.add_pattern(0)
		self.pattern_list.add_pattern(1,test_seq, 8)
		self.pattern_list.add_pattern(2)
		self.pattern_list.add_pattern(3)
		self.pattern_list.add_pattern(4)
		self.pattern_list.pattern_editing(0, 'John')
		self.pattern_list.pattern_editing(1, 'Bob')

		# i2player = Window.width/len(self.players)
		# scale = 1./len(self.players)
		# for i, player in enumerate(self.players):
		# 	player.position.x = i2player*i+80
		# 	player.scale.x = scale
		# 	self.IM.add(player.instrument)
		# 	continue
		# self.current_player = 0
		# self.num_players = len(self.players)

		# self.add(*self.players)
		self.add(self.IM)

		self.clock.offset = self.seconds-spb
		print self.clock.offset
		# self.clock.start()
		self.IM.metro.start()
		self.paused = True
		self.start()

	def on_key_down(self, event):
		# if event.keycode[1] == 'enter':on
		# 	self.toggle() 
		pass

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
		

	def next_player(self, sequence):
		if self.current_player < self.num_players:
			self.players[self.current_player].note_sequence = sequence
			self.players[self.current_player].stop_composing()
			self.current_player += 1
		if self.current_player < self.num_players:
			self.players[self.current_player].start_composing()

	def on_lock_in(self, event):
		self.next_player(event.action['sequence'])

	def on_update(self):
		self.sched.on_update()
		# for player in self.players:
		self.player.set_now(self.clock.get_time()%self.seconds)
		self.pattern_list.set_now(self.clock.get_time()%self.seconds)