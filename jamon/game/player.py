from game import GameObject

from instrument import *
from components.sprites import *

from text import TextObject


from kivy.core.window import Window

# assert([len(dk) == num_lanes for dk in default_keys])

statuses = {
	1: 'Create a Pattern!',
	2: 'Locked in!',
}

class VirtualPlayer(GameObject):
	def __init__(self, controller, track):
		super(VirtualPlayer, self).__init__()

		self.controller = controller
		self.add(controller)		

		self.controller.bind_notes(self.key_down_cb, self.key_up_cb)
		self.controller.bind_lock_in(self.lock_in)

		self.track = track
		self.add(track)

		self.active_pattern = None
		self.note_sequence = []
		self.seq_ind = 0

		self.time = 0
		self.last_time = 0
		self.status = 0

		self.composing = False

	def lock_in(self):
		if self.track.active:
			self.active_pattern.lock_in()
			self.track.set_active(False)

	@property
	def id(self):
		return self.controller.vid if self.controller else None

	def start_composing(self):
		if self.composing:
			return
		self.composing = True

	def stop_composing(self):
		if not self.composing:
			return
		self.composing = False
		# if self.is_me:
		# 	self.set_status(2)

	def key_down_cb(self, lane_num):
		def cb():
			self.key_down(lane_num)
		return cb

	def key_up_cb(self, lane_num):
		def cb():
			self.key_up(lane_num)
		return cb

	def key_down(self, lane_num):
		self.track.on_press(lane_num)

	def key_up(self, lane_num):
		self.track.on_release(lane_num)

	def set_active_pattern(self, pattern):
		self.active_pattern = pattern

	def set_now(self, time):
		self.track.set_now(time)
		self.time = time

	def on_update(self):
		if self.time < self.last_time:
			self.seq_ind = 0
		self.last_time = self.time

	@property
	def session(self):
		return self._parent


class Player(VirtualPlayer):
	# def __init__(self, server_obj, name, is_me, bars, tempo, num=0, inst='piano'):
	def __init__(self, controller, track, inst_set):
		super(Player, self).__init__(controller, track)
		print inst_set
		inst = INSTRUMENT_SETS[inst_set].keys()[0]

		self.instrument = Instrument(inst)

		self.status_sprite = None
		self.action_buffer = []
		self.start_composing()

	@property
	def num_notes(self):
		return len(self.instrument.notes)

	def key_down(self, lane_num):
		super(Player, self).key_down(lane_num)
		if lane_num < self.num_notes:
			self.instrument.note_on(lane_num)

	def key_up(self, lane_num):
		super(Player, self).key_up(lane_num)
		if lane_num < self.num_notes:
			self.instrument.note_off(lane_num)

	def set_inst(self, inst, inst_set=None):
		self.instrument.set_inst(inst, inst_set)
		self.track.update_lanes(self.num_notes)

	def on_update(self):
		super(Player, self).on_update()
		# Play notes if not composing
		if not self.composing and len(self.note_sequence) > 0:
			if self.seq_ind < len(self.note_sequence):
				next_time, notes = self.note_sequence[self.seq_ind]
				if next_time <= self.time:
					# print self.time
					for (lane, onoff) in notes:
						if onoff == 'on':
							# print "NOTE ON", lane
							self.instrument.note_on(lane)
						elif onoff == 'off':
							# print "NOTE OFF", lane
							self.instrument.note_off(lane)
					self.seq_ind  += 1
