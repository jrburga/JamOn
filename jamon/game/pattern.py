from jamon.game.game import GameObject
from components.sprites import *
from jamon.game.window import Window
from widgets import Button
from kivy.core.image import Image
from text import TextObject
from instrument import Instrument
from kivy.clock import Clock as kivyClock

class PatternList(GameObject):

	def __init__(self, bars, tempo):
		super(PatternList, self).__init__()

		self.bars = bars
		self.tempo = tempo

		self.patterns = {}

		self.scroll = ScrollView()
		# self.add_btn = PatternButton('add', self.add_btn_clicked)
		# self.add_btn.position = (5, pattern_list_height-80)
		# self.scroll.add(self.add_btn)
		self.add(self.scroll)

		self.inst_panel = InstrumentPanel()
		self.add(self.inst_panel)

		self.sprite = PatternListSprite()
		self.add_graphic(self.sprite)



	def send_event(self, msg):
		# This is where it will call the server to send the message

		# FOR DEBUGGING PURPOSES
		if msg['event']=='add':
			import random
			_id = random.randint(0, 100000)
			self.create_pattern(_id, msg['inst'])
		elif msg['event']=='remove':
			self.remove_pattern(msg['id'])
		elif msg['event']=='queue':
			self.set_queued(msg['id'])
		elif msg['event']=='dequeue':
			self.set_dequeued(msg['id'])
		elif msg['event']=='done_edit':
			self.pattern_done_editing(msg['id'], msg['seq'])
	
	# Called when the user begins creating a new pattern
	def create_pattern(self, _id, inst):
		# Add a patten to the top of the list
		pattern = Pattern(_id, 0, self.bars, self.tempo, [], inst, self._parent.IM)

		# Shift index of all other patterns down
		for k in self.patterns:
			p = self.patterns[k]
			p.idx += 1
			p.move_to(p.position.y - pattern_height - spacing)

		# Add pattern to dict
		self.patterns[_id] = pattern

		# Tell pattern it's being edited
		pattern.editing(is_me=True)

		# Add pattern to the screen
		self.scroll.add(pattern)

		# Give the track the pattern info to update the midi live
		track = self._parent.player.track
		track.set_active_pattern(pattern)

		# Set the instrument to the correct instrument
		self._parent.player.instrument.set_inst(inst)

	def remove_pattern(self, _id):
		pattern = self.patterns[_id]
		idx = pattern.idx
		self.scroll.remove(pattern)
		del self.patterns[_id]

		# Shift everything below the pattern up
		for k in self.patterns:
			p = self.patterns[k]
			if p.idx > idx:
				p.move_to(p.position.y + pattern_height + spacing)

		# Shift add button up
		# self.add_btn.position.y += pattern_height + spacing



	def add_pattern(self, _id, seq=[], inst='piano'):
		idx = len(self.patterns)
		pattern = Pattern(_id, idx, self.bars, self.tempo, seq, inst, self._parent.IM)
		self.scroll.add(pattern)
		self.patterns[_id] = pattern

		# move add button down
		# self.add_btn.position.y -= (pattern_height + spacing)

	def set_queued(self, pattern):
		self.patterns[pattern].set_queued()

	def set_dequeued(self, pattern):
		self.patterns[pattern].set_dequeued()

	def pattern_editing(self, pattern, editor):
		self.patterns[pattern].editing(editor)

	def pattern_done_editing(self, pattern, seq):
		self.patterns[pattern].done_editing(seq)

	def set_now(self, now):
		for k in self.patterns:
			self.patterns[k].set_now(now)


class InstrumentPanel(GameObject):
	def __init__(self):
		super(InstrumentPanel, self).__init__()

		self.sprite = InstrumentPanelSrite()
		self.add_graphic(self.sprite)

		self.inst_btns = [PatternButton(inst, self.get_inst_btn_callback(i)) for i, inst in enumerate(('guitar', 'piano', 'drum', 'vibraphone'))]
		for i, e in enumerate(self.inst_btns):
			e.position = (70 + i * 70, -20)
			self.add(e)

		self.active_idx = None

	def deactivate(self):
		if self.active_idx is None:
			return
		btn = self.inst_btns[self.active_idx]
		btn.sprite.color.rgb = (1,1,1)
		btn.sprite.color.v = 0.5
		self.active_idx = None

	def get_inst_btn_callback(self, idx):
		def cb():
			btn = self.inst_btns[idx]
			print btn.typ + ' called!'
			track = self._parent._parent.player.track
			if not track.active:
				track.set_active(True)
				btn.sprite.color.rgb = (0,1,0)
				btn.sprite.color.v = 0.5
				self.active_idx = idx
				self._parent.send_event({'event':'add', 'inst':btn.typ})

		return cb



class ScrollView(GameObject):
	def __init__(self):
		super(ScrollView, self).__init__()
		self.up = False
		self.down = False

		self.objects_to_remove = []

	def remove(self, obj):
		self.objects_to_remove.append(obj)


	def on_key_down(self, event):
		if event.keycode[1] == 'down':
			self.down = True
		elif event.keycode[1] == 'up':
			self.up = True

	def on_key_up(self, event):
		if event.keycode[1] == 'down':
			self.down = False
		elif event.keycode[1] == 'up':
			self.up = False

	def on_update(self):
		if self.down and self.up:
			return
		if self.down:
			self.position.y += 5
		if self.up:
			if self.position.y > 5:
				self.position.y -= 5

		# Remove items
		for obj in self.objects_to_remove:
			super(ScrollView, self).remove(obj)
		self.objects_to_remove = []


class PatternNote(GameObject):
	def __init__(self, lane, start, length, seconds, num_lanes):
		super(PatternNote, self).__init__()
		self.start = start
		self.length = length
		self.lane = lane
		self.seconds = seconds
		self.num_lanes = num_lanes

		size_x = pattern_size[0] / self.seconds * length
		size_y = pattern_size[1] / self.num_lanes - 2
		sprite = PatternNoteSprite( (size_x, size_y) )
		self.add_graphic(sprite)

		self.position.xy = (start * pattern_size[0] / self.seconds, lane * pattern_size[1] / self.num_lanes)


spacing = 50

class Pattern(GameObject):

	def __init__(self, _id, idx, bars, tempo, seq, inst, IM):
		super(Pattern, self).__init__()
		self._id = _id
		self.bars = bars
		self.tempo = tempo
		self.seq = seq
		self.note_sprites = {}
		self.figure_notes()
		self.note_idx = 0
		self.last_time = 0
		self.idx = idx
		self.instrument = Instrument(inst)
		IM.add(self.instrument)
		self.num_lanes = len(self.instrument.notes)
		self.now = 0
		self.run_time = 0
		self.spb = 60./tempo
		beats = bars*4
		self.seconds = self.spb*beats

		self.notes = {} # key = (start, lane)
		for (lane, start, length) in seq:
			note = PatternNote(lane, start, length, self.seconds, self.num_lanes)
			self.notes[ (start, lane) ] = note
			self.add(note)

		self.old_notes = {}

		

		# Display the pattern outline
		self.outline_sprite = PatternOutlineSprite()
		self.outline_sprite.color.v = 0.5
		self.outline_sprite.color.h = .55
		self.add_graphic(self.outline_sprite)
		
		self.position.x = 5
		self.position.y = pattern_list_height - (pattern_height + spacing) * (1 + idx)

		# Create the nowbar
		self.now_bar = PatternNowBarSprite()
		self.add_graphic(self.now_bar)

		# Display MIDI
		# self.display_midi()

		# Display pattern buttons
		self.play_btn = PatternScrollButton('play', self.on_play_click)
		self.add(self.play_btn)
		self.delete_btn = PatternScrollButton('delete', self.on_delete_click)
		self.delete_btn.position.x += 35
		self.add(self.delete_btn)

		# Display instrument icon
		inst_sprite = PatternInstrumentIconSprite(inst + '.png')
		inst_sprite.position = (80,52)
		self.add_graphic(inst_sprite)


		# STATE: 0: muted, 1: queued, 2: playing, 4: de-queued
		self.state = 0

		self.locked = False
		self.is_editing = False

		self.info_text = None

		self.sprites_to_remove = []
		self.objects_to_remove = []

		# For animation
		self.anim = None

	# For animated scrolling	
	def move_to(self, y):
		self.anim = KFAnim( (self.run_time, self.position.y), (self.run_time + 0.3, y))

	# Adds a note to the mid
	def add_note(self, start, length, lane):
		note = PatternNote(lane, start, length, self.seconds, self.num_lanes)
		self.notes[ (start, lane) ] = note
		self.add(note)


	def remove_note(self, start, lane):
		if (start, lane) not in self.old_notes:
			print 'something went wrong... (Pattern.remove_note)'
			return
		note = self.old_notes[ (start, lane) ]
		self.remove(note)
		# del self.old_notes[ (start, lane) ]

	def new_phrase(self):
		# Move notes to old notes
		self.old_notes = self.notes
		self.notes = {}

	# Called when the user is done editing this pattern
	def lock_in(self):
		# Create seq list from old notes
		self.seq = []
		for k in self.old_notes:
			note = self.old_notes[k]
			self.seq.append( (note.lane, note.start, note.length) )

		# Queue the pattern
		self._parent._parent.send_event({'event':'done_edit', 'id':self._id, 'seq':self.seq})

		# Show instrument button as unclicked
		self._parent._parent.inst_panel.deactivate()




	def figure_notes(self):
		note_dict = {}
		for (lane, start, length) in self.seq:
			end = start + length
			if start not in note_dict:
				note_dict[start] = [('on', lane)]
			else:
				note_dict[start].append(('on', lane))
			if end not in note_dict:
				note_dict[end] = [('off', lane)]
			else:
				note_dict[end].append(('off', lane))
		self.note_events = []
		for time in sorted(note_dict.iterkeys()):
			self.note_events.append( (time, note_dict[time]) )


	# Creates note_sprites list and displays sprites based on self.seq
	# def display_midi(self):
	# 	self.note_sprites = {}
	# 	for (lane, start, length) in self.seq:
	# 		size_x = pattern_size[0] / self.seconds * length
	# 		size_y = pattern_size[1] / self.num_lanes - 2
	# 		sprite = PatternNoteSprite( (size_x, size_y) )
	# 		sprite.position = (start * pattern_size[0] / self.seconds, lane * pattern_size[1] / self.num_lanes)
	# 		self.note_sprites[(lane, start)] = sprite
	# 		self.add_graphic(sprite)


	def on_play_click(self):
		if self.is_editing:
			return
		event = 'queue' if self.state in (0,3) else 'dequeue'
		self._parent._parent.send_event({'event':event, 'id':self._id})

	def on_delete_click(self):
		if self.is_editing:
			return

		# TO IMPLEMENT LATER: DELETING TRACK BEFORE YOU FINISH EDITING IT
		# if self.is_editing:
		# 	# This means the current player is editing this pattern and deleting it before it's done
		# 	self._parent._parent.player.track.set_active(False)
		# 	self._parent._parent
		self._parent._parent.send_event({'event': 'remove', 'id': self._id})

	def set_queued(self):
		if self.state == 3: #formerly dequeued
			self.set_active()
			return
		self.state = 1
		self.outline_sprite.color.v = 1
	 	self.outline_sprite.color.h = 0.7

	def set_dequeued(self):
		if self.state == 1: #formerly queued (never played)
			self.set_inactive()
			return
		self.state = 3
	 	self.outline_sprite.color.v = 0.5
	 	self.outline_sprite.color.h = 0.7

	def set_active(self):
		self.state = 2
	 	self.outline_sprite.color.v = 1
	 	self.outline_sprite.color.h = 0.9

	def set_inactive(self):
	 	self.state = 0
	 	self.outline_sprite.color.v = 0.5
	 	self.outline_sprite.color.h = 0.55

	def editing(self, editor='', is_me=False):
		self.locked = not is_me
		self.is_editing = True
		self.outline_sprite.color.v = 1
		self.outline_sprite.color.h = 0

		if self.info_text is not None:
			self.objects_to_remove.append(self.info_text)
		if not is_me:
			self.info_text = TextObject(editor+' is editing...', font_size=14, color=self.outline_sprite.color.rgb)
		else:
			self.info_text = TextObject('You are editing...', font_size=14, color=self.outline_sprite.color.rgb)
		self.info_text.position = (200, pattern_height)
		self.add(self.info_text)

	def done_editing(self, seq):
		self.seq = seq
		for ns in self.note_sprites:
			self.sprites_to_remove.append(ns)
		self.locked = False
		self.is_editing = False
		if self.info_text is not None:
			self.objects_to_remove.append(self.info_text)
		self.figure_notes()
		# Draw new notes
		for k in self.notes:
			if k not in self.old_notes:
				self.remove(self.notes[k])
		for k in self.old_notes:
			if self.old_notes[k]._parent is None:
				self.add(self.old_notes[k])
		self.set_queued()

	def time2x(self, t):
		return pattern_size[0]*t/self.seconds

	def set_now(self, now):
		self.now = now

	def on_update(self):
		# Needs to be handled synchronously and not from events
		for s in self.sprites_to_remove:
			# I had to do this because of a weird KeyError....
			if s in self._graphics._objects:
				self.remove_graphic(s)
		for o in self.objects_to_remove:
			self.remove(o)


		# Move now bar
		_, y = self.now_bar.position
		x = self.time2x(self.now)
		self.now_bar.position = (x, y)

		

		# See if new bar happened
		if self.now < self.last_time:
			self.note_idx = 0

			#Queue-dequeue
			if self.state == 1:
				self.set_active()
			elif self.state == 3:
				self.set_inactive()

		# Set mute if active or not
		self.instrument.set_mute(self.state < 2)

		# Play the notes
		if self.note_idx < len(self.note_events):
			time, events = self.note_events[self.note_idx]
			if self.now > time:
				self.note_idx += 1
				for (onoff, lane) in events:
					if onoff == 'on':
						self.instrument.note_on(lane)
					else:
						self.instrument.note_off(lane)
		self.last_time = self.now

		# Animate
		if self.anim is not None:
			self.position.y = self.anim.eval(self.run_time)
		self.run_time += kivyClock.frametime



class PatternButton(GameObject):
	def __init__(self, typ, callback):
		super(PatternButton, self).__init__()
		self.typ = typ
		self.callback = callback
		self.sprite = None
		self.touched = False
		
		if self.sprite is not None:
			self.remove_graphic(self.sprite)

		if self.typ == 'play':
			self.sprite = PatternPlaySprite()
		elif self.typ == 'add':
			self.sprite = PatternAddSprite()
		elif self.typ == 'delete':
			self.sprite = PatternDeleteSprite()
		elif self.typ in ('guitar', 'drum', 'vibraphone', 'piano'):
			self.sprite = PatternInstrumentSprite(self.typ + '.png')

		self.sprite.position = (5, pattern_height)
		self.sprite.color.v = 0.5
		self.add_graphic(self.sprite)

		self.events = []


	def on_touch_down(self, event):
		x, y = event.touch.pos
		self.figure_pos()
		if abs(x - self.x) < self.sprite.size[0]/2 and abs(y - self.y) < self.sprite.size[1]/2:
			self.touched = True
			self.sprite.color.v = 1

	def on_touch_up(self, event):
		if self.touched:
			self.touched = False
			self.events.append(self.callback)
			self.sprite.color.v = 0.5


	def figure_pos(self):
		x, y = self.get_abs_pos()
		x += 5 + self.sprite.size[0]/2
		y += pattern_height + self.sprite.size[1]/2
		self.x = x
		self.y = y

	def on_update(self):
		while self.events:
			self.events.pop(0)()


# Wrapper class so buttons in the scroll view can't be clicked when they go
# behind the instrument panel at the bottom of the screen
class PatternScrollButton(PatternButton):
	def __init__(self, typ, callback):
		super(PatternScrollButton, self).__init__(typ, callback)

	def on_touch_down(self, event):
		y = event.touch.pos[1]
		# Check if the click happened above the top of the instrument panel
		if y > 100:
			super(PatternScrollButton, self).on_touch_down(event)








