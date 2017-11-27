from game import GameObject

from controller import Keyboard
from instrument import Instrument
from track import Track

num_lanes = 8
default_keys = [
	['a', 's', 'd', 'f', 'q', 'w', 'e', 'r', ' '], 
	['a', 's', 'd', 'f', 'q', 'w', 'e', 'r', ' '],
	['j', 'k', 'l', ';', 'u', 'i', 'o', 'p', ' ']
]

# assert([len(dk) == num_lanes for dk in default_keys])

default_keys = [[ord(k) for k in dk] for dk in default_keys]

class Player(Keyboard):
	def __init__(self, bars, tempo, num=0, inst='piano'):
		super(Player, self).__init__()
		self.keys = default_keys[num]
		self.instrument = Instrument(inst)

		self.note_sequence = []
		self.seq_ind = 0
		self.last_time = 0

		perc = True if inst=='drums' else False
		self.track = Track(num_lanes, bars, tempo, percussive=perc)

		self.composing = False
		if num == 0:
			self.composing = True

		self.num = num
		self.time = 0
		self.add(self.track)

	def key_down(self, lane_num):
		if lane_num == num_lanes:
			if self.composing:
				self.lock_in_sequence()
			return

		if self.composing:
			self.track.on_press(lane_num)
		self.instrument.note_on(lane_num)

	def key_up(self, lane_num):
		if lane_num == num_lanes:
			return

		if self.composing:
			self.track.on_release(lane_num)
		self.instrument.note_off(lane_num)

	def set_now(self, time):
		self.track.set_now(time)
		self.time = time

	def on_update(self):
		# Play notes if not composing
		if self.time < self.last_time:
			self.seq_ind = 0

		if not self.composing and len(self.note_sequence) > 0:
			if self.seq_ind < len(self.note_sequence):
				next_time, notes = self.note_sequence[self.seq_ind]
				if next_time <= self.time:
					print self.time
					for (lane, onoff) in notes:
						if onoff == 'on':
							print "NOTE ON", lane
							self.instrument.note_on(lane)
						elif onoff == 'off':
							print "NOTE OFF", lane
							self.instrument.note_off(lane)
					self.seq_ind  += 1

		self.last_time = self.time

	@property
	def session(self):
		return self._parent

	def lock_in_sequence(self):
		# set note_sequence
		notes = {}
		for i, lane in enumerate(self.track.lanes):
			print 'locked:', lane.locked_times
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

		self.composing = False
		self.trigger_event('on_lock_in')



