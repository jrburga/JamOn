from game import GameObject

from controller import Keyboard
from instrument import Instrument
from track import Track
from components.sprites import PlayerOutlineSprite, PlayerNameSprite, PlayerStatusSprite

from kivy.core.window import Window

num_lanes = 8
default_keys = [
	['a', 's', 'd', 'f', 'q', 'w', 'e', 'r', ' '], 
	['a', 's', 'd', 'f', 'q', 'w', 'e', 'r', ' '],
	['j', 'k', 'l', ';', 'u', 'i', 'o', 'p', ' ']
]

# assert([len(dk) == num_lanes for dk in default_keys])

default_keys = [[ord(k) for k in dk] for dk in default_keys]

statuses = {
	1: 'Create a Pattern!',
	2: 'Locked in!',
}

class Player(Keyboard):
	def __init__(self, server_obj, name, is_me, bars, tempo, num=0, inst='piano'):
		super(Player, self).__init__()
		self.keys = default_keys[num]
		self.instrument = Instrument(inst)

		# Boolean that represents whether this Player object correlates to
		# the player for this system. I think this won't be needed once we 
		# make other players use a different controller...
		self.is_me = is_me

		self.name = name

		self.note_sequence = []
		self.seq_ind = 0
		self.last_time = 0

		perc = True if inst=='drums' else False
		self.track = Track(num_lanes, bars, tempo, percussive=perc)
		self.track.position.x = 5
		self.track.position.y = Window.height*0.005

		

		self.num = num
		self.time = 0

		self.add_graphic(PlayerOutlineSprite(is_me))
		self.add_graphic(PlayerNameSprite(name, is_me))

		self.status = 0
		self.status_sprite = None

		self.composing = False
		if num == 0:
			self.start_composing()

		self.add(self.track)


	def start_composing(self):
		if self.composing:
			return
		self.composing = True
		if self.is_me:
			self.set_status(1)

	def stop_composing(self):
		if not self.composing:
			return
		self.composing = False
		if self.is_me:
			self.set_status(2)


	def set_status(self, status):
		self.status = status
		if self.status_sprite is not None:
			self.remove_graphic(self.status_sprite)
		if status in statuses:
			self.status_sprite = PlayerStatusSprite(statuses[status])
			self.add_graphic(self.status_sprite)
		else:
			self.status_sprite = None

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

		self.trigger_event('on_lock_in')

class PlayerRemote(Player):
	def __init__(self, name, is_me, bars, tempo, num=0, inst='piano'):
		super(PlayerRemote, self).__init__(name, is_me, bars, tempo, num, inst)
		self.keys = []

	# overwrite these
	def on_key_down(self, event):
		pass

	def on_key_up(self, event):
		pass

	def on_msg_recieve(self, event):
		print event


