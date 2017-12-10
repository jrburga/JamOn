from game import GameObject
from track import *
from player import Player, VirtualPlayer
from controller import InstrumentKeyboard, InstrumentController
from instrument import InstrumentManager
from pattern import PatternList	
from kivy.clock import Clock as kivyClock
from kivy.core.window import Window
from components.sprites import *

from common.clock import Clock, Scheduler, SimpleTempoMap

num_lanes = 8

default_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']
lockin_key = ' '

default_keycodes = [ord(k) for k in default_keys]
lock_in_keycode = ord(lockin_key)

class Session(GameObject):
	def __init__(self, other_members, tempo, bars, divs):
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
		self.add(self.IM)

		### NEW CODE ###
		self.pattern_list = PatternList(self.bars, self.tempo)
		self.add(self.pattern_list)

		track = Track(num_lanes, self.bars, self.tempo)
		track.position.y = Window.height*0.01
		controller = InstrumentKeyboard(default_keycodes, 
										lock_in_keycode)
		self.player = Player(controller, track)
		self.player.position.x = Window.width - player_size[0] - 20
		self.add(self.player)
		self.vplayers = []
		self.add_band_members(other_members)
		self.IM.add(self.player.instrument)

		self.clock.offset = self.seconds-spb

		self.paused = True
		self.start()

	def add_band_members(self, other_members):
		print 'getting band_members'
		print '===================='
		print other_members
		for other_member in other_members:
			vcontroller = InstrumentController(8, other_member['id'])
			vtrack = VirtualTrack(num_lanes, self.bars, self.tempo)
			vplayer = VirtualPlayer(vcontroller, vtrack)
			self.vplayers.append(vplayer)
			self.add(vplayer)

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
		now = self.clock.get_time()%self.seconds
		for vplayer in self.vplayers:
			vplayer.set_now(now)
		self.player.set_now(now)
		self.pattern_list.set_now(self.clock.get_time()%self.seconds)
