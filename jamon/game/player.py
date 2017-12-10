from game import GameObject

from instrument import Instrument
from components.sprites import *

from text import TextObject


from kivy.core.window import Window

# assert([len(dk) == num_lanes for dk in default_keys])

statuses = {
	1: 'Create a Pattern!',
	2: 'Locked in!',
}

default_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']

default_keycodes = [ord(k) for k in default_keys]

class Editor(GameObject):
	def __init__(self, controller):
		super(Editor, self).__init__()
		self.controller = controller
		self.add(controller)

		self.active_pattern = None
		self.note_sequence = []
		self.seq_ind = 0

		self.time = 0
		self.last_time = 0
		self.status = 0

		self.composing = False

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

	def key_down(self, lane_num):
		if self.composing:
			self.track.on_press(lane_num)

	def key_up(self, lane_num):
		if self.composing:
			self.track.on_release(lane_num)

	def set_active_pattern(self, pattern):
		self.active_pattern = pattern

	def set_now(self, time):
		self.track.set_now(time)
		self.time = time

	def lock_in_sequence(self):
		print 'locking in sequence'

		# set note_sequence
		if self.is_me:
			print 'locking in sequence'
			notes = {}
			for i, lane in enumerate(self.track.lanes):
				# print 'locked:', lane.locked_times
				for (time, length) in lane.locked_times:
					end_time = time + length
					if time not in notes:
						notes[time] = []
					notes[time].append( (i, 'on') )
					if end_time not in notes:
						notes[end_time] = []
					notes[end_time].append( (i, 'off') )
			# sort the note sequence
			for k in sorted(notes.iterkeys()):
				self.note_sequence.append( (k, notes[k]) )
		print self.note_sequence

	def on_update(self):
		if self.time < self.last_time:
			self.seq_ind = 0
		self.last_time = self.time


class Player(Editor):
	# def __init__(self, server_obj, name, is_me, bars, tempo, num=0, inst='piano'):
	def __init__(self, controller, track, inst='piano'):
		super(Player, self).__init__(controller)
		self.instrument = Instrument(inst)

		for i, keycode in enumerate(default_keycodes):
			print i, keycode
			self.controller.bind_keydown(keycode, self.key_down_cb(i))
			self.controller.bind_keyup(keycode, self.key_up_cb(i))

		self.controller.bind_keydown(32, self.space_bar_pressed)

		self.track = track
		self.add(self.track)
		self.status_sprite = None
		self.action_buffer = []
		self.start_composing()

	def space_bar_pressed(self):
		if self.track.active:
			self.active_pattern.lock_in()
			self.track.set_active(False)


	def set_status(self, status):
		self.status = status
		if self.status_sprite is not None:
			self.remove(self.status_sprite)
		if status in statuses:
			self.status_sprite = PlayerStatusText(statuses[status])
			self.add(self.status_sprite)
		else:
			self.status_sprite = None

	def key_down_cb(self, lane_num):
		def cb():
			self.key_down(lane_num)
		return cb

	def key_up_cb(self, lane_num):
		def cb():
			self.key_up(lane_num)
		return cb

	def key_down(self, lane_num):
		super(Player, self).key_down(lane_num)
		self.instrument.note_on(lane_num)

	def key_up(self, lane_num):
		super(Player, self).key_up(lane_num)
		self.instrument.note_off(lane_num)


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

		self.last_time = self.time

	@property
	def session(self):
		return self._parent


class VirtualPlayer(Player):
	def __init__(self, vcontroller, vtrack):
		super(VirtualPlayer, self).__init__()


# class PlayerNameText(TextObject):
# 	def __init__(self, name, me):
# 		color = (.3, .6, .3) if me else (.4, .4, .4)
# 		super(PlayerNameText, self).__init__(name, color=color, pos=(20,player_size[1]*.95))

# class PlayerStatusText(TextObject):
# 	def __init__(self, status):
# 		color = (.3, .6, .3)
# 		super(PlayerStatusText, self).__init__(status, color=color, pos=(120,player_size[1]*.95))


