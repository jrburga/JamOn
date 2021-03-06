from jamon.game.game import GameObject
from components.sprites import *
from jamon.game.window import Window
from widgets import Button
from kivy.core.image import Image
from text import TextObject
from instrument import *
from kivy.clock import Clock as kivyClock

class PatternList(GameObject):

	def __init__(self, bars, tempo, inst_set):
		super(PatternList, self).__init__()

		self.bars = bars
		self.tempo = tempo
		self.inst_set = inst_set

		self.patterns = {}

		self.editing_id = None

		self.scroll = ScrollView()
		# self.add_btn = PatternButton('add', self.add_btn_clicked)
		# self.add_btn.position = (5, pattern_list_height-80)
		# self.scroll.add(self.add_btn)
		self.add(self.scroll)

		self.inst_panel = InstrumentPanel(inst_set)
		self.add(self.inst_panel)

		self.sprite = PatternListSprite()
		self.add_graphic(self.sprite)

	def send_event(self, msg):
		# FOR DEBUGGING PURPOSES
		if msg['event']=='add':
			self.create_pattern(msg['inst'])
		elif msg['event']=='remove':
			self.remove_pattern(msg['id'])
		elif msg['event']=='queue':
			self.set_queued(msg['id'])
		elif msg['event']=='dequeue':
			self.set_dequeued(msg['id'])
		elif msg['event']=='done_edit':
			self.pattern_done_editing(msg['id'], msg['seq'])


	def create_pattern(self, inst):
		# self.client.send_action('on_pattern_create', id=_id, inst=msg['inst'], creator=creator)
		_id = self.client.add_pattern(inst)
		creator = self.client.info
		self.client.send_action('on_pattern_create', pattern_id=_id, 
								 inst=inst, creator=self.client.info)

	def on_pattern_create(self, event):
		_id = event.pattern_id
		inst = event.inst
		creator = event.creator
		is_me = creator['id']==self.client.id
		username = creator['username']



		pattern = self.add_pattern(_id, inst=inst)
		pattern.editing(editor=username, is_me=is_me)
		# Give the track the pattern info to update the midi live
		# We should give the "player" the pattern, 
		# since they are the ones controlling it
		if is_me:
			player = self._parent.player
			player.set_active_pattern(pattern)

			# Set the instrument to the correct instrument
			self._parent.player.set_inst(inst, self.inst_set)

		for vplayer in filter(lambda p: p.id == creator['id'], self._parent.vplayers):
			vplayer.track.set_active(True)
			vplayer.set_active_pattern(pattern)

	def remove_pattern(self, _id):
		self.client.delete_pattern(_id)
		self.client.send_action('on_pattern_remove', pattern_id=_id)

	def on_pattern_remove(self, event):
		_id = event.pattern_id
		pattern = self.patterns[_id]
		idx = pattern.idx
		# Make sure to stop playing the notes in the pattern
		pattern.shut_off()

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
		# Add a pattern to the top of the list
		pattern = Pattern(_id, 0, self.bars, self.tempo, seq, inst, self.inst_set, self._parent.IM)

		# Shift index of all other patterns down
		for k in self.patterns:
			p = self.patterns[k]
			p.idx += 1
			p.move_to(p.position.y - pattern_height - spacing)

		self.patterns[_id] = pattern
		self.scroll.add(pattern)

		return pattern

		# move add button down
		# self.add_btn.position.y -= (pattern_height + spacing)

	def set_queued(self, pattern):
		self.client.send_action('on_set_queue', pattern=pattern)

	def on_set_queue(self, event):
		pattern = event.pattern
		self.patterns[pattern].set_queued()

	def set_dequeued(self, pattern):
		self.client.send_action('on_set_dequeued', pattern=pattern)

	def on_set_dequeued(self, event):
		pattern = event.pattern
		self.patterns[pattern].set_dequeued()

	def pattern_editing(self, pattern, editor):
		self.patterns[pattern].editing(editor)

	def pattern_done_editing(self, pattern, seq):
		self.client.send_action('on_pattern_done_editing', pattern_id=pattern, seq=seq)

	def on_pattern_done_editing(self, event):
		pattern_id = event.pattern_id
		seq = event.seq
		self.patterns[pattern_id].done_editing(seq)

	def set_now(self, now):
		for k in self.patterns:
			self.patterns[k].set_now(now)


class InstrumentPanel(GameObject):
	def __init__(self, inst_set):
		super(InstrumentPanel, self).__init__()
		self.inst_set = inst_set
		self.insts = INSTRUMENT_SETS[inst_set].keys()
		self.sprite = InstrumentPanelSrite()
		self.add_graphic(self.sprite)
		self.inst_btns = [PatternButton(inst, self.get_inst_btn_callback(i)) for i, inst in enumerate(self.insts)]
		for i, e in enumerate(self.inst_btns):
			e.position = (70 + i * 70, - inst_panel_size[1]*0.9)
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
		self.sprite = PatternNoteSprite( (size_x, size_y) )
		self.add_graphic(self.sprite)

		self.position.xy = (start * pattern_size[0] / self.seconds, lane * pattern_size[1] / self.num_lanes)


spacing = 50

class Pattern(GameObject):

	def __init__(self, _id, idx, bars, tempo, seq, inst, inst_set, IM):
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
		self.instrument = Instrument(inst, inst_set)
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
		inst_sprite.position = (80,pattern_height+1)
		self.add_graphic(inst_sprite)

		# Display volume slider
		self.volume = 1
		self.vol_slider = VolumeSlider(self.volume, self.on_volume_change)
		self.add(self.vol_slider)


		# STATE: 0: muted, 1: queued, 2: playing, 4: de-queued
		self.state = 0

		self.locked = False
		self.is_editing = False

		self.info_text = None

		self.sprites_to_remove = []
		self.objects_to_remove = []

		# For animation
		self.anim = None

	# All noted playing are stopped
	def shut_off(self):
		for i in range(self.num_lanes):
			self.instrument.note_off(i)

	# Callback for volume slider
	def on_volume_change(self, volume):
		self.volume = volume
		self.instrument.set_volume(volume)

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
		notes = self.notes if self.notes else self.old_notes
		for k in notes:
			note = notes[k]
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
		self.outline_sprite.color.rgb = YELLOW + (0.2,)

		for note in self.notes.values():
			note.sprite.color.rgb = invert_color(YELLOW)

	def set_dequeued(self):
		if self.state == 1: #formerly queued (never played)
			self.set_inactive()
			return
		self.state = 3
	 	self.outline_sprite.color.rgb = RED
		for note in self.notes.values():
	 		note.sprite.color.rgb = invert_color(RED)

	def set_active(self):
		self.state = 2
	 	self.outline_sprite.color.rgb = GREEN + (0.6,)
	 	
		for note in self.notes.values():
			note.sprite.color.rgb = invert_color(GREEN)

	def set_inactive(self):
	 	self.state = 0
	 	self.outline_sprite.color.rgba = (0,0,0,0.3)
		for note in self.notes.values():
			note.sprite.color.rgb = invert_color((0,0,0))

	def editing(self, editor='', is_me=False):
		self.locked = not is_me
		self.is_editing = True
		self.outline_sprite.color.rgb = BLUE + (0.6,)

		if self.info_text is not None:
			self.objects_to_remove.append(self.info_text)
		if not is_me:
			self.info_text = TextObject(editor+' is editing...', font_size=28, color=(0,0,0))
		else:
			self.info_text = TextObject('You are editing...', font_size=28, color=(0,0,0))
		self.info_text.position = (300, pattern_height)
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

		# Remove old notes from screen
		for k in self.notes:
			self.remove(self.notes[k])
		for k in self.old_notes:
			if self.old_notes[k]._parent is not None:
				self.remove(self.old_notes[k])
		self.notes = {}
		self.old_notes = {}

		self.note_idx = 0

		# Draw new notes
		for (lane, start, length) in seq:
			note = PatternNote(lane, start, length, self.seconds, self.num_lanes)
			self.notes[ (start, lane) ] = note
			self.add(note)

			# Set the note index to the right spot
			if self.now > start:
				self.note_idx += 1

		self.note_idx = min(self.note_idx, len(self.notes)-1)

		self.set_active()


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
			# Make sure events at end happen
			if self.note_events:
				time, events = self.note_events[-1]
				for (onoff, lane) in events:
					if onoff == 'off':
							self.instrument.note_off(lane)

			# Reset index pointer
			self.note_idx = 0

			#Queue-dequeue
			if self.state == 1:
				self.set_active()
			elif self.state == 3:
				self.set_inactive()

		# Set mute if active or not
		self.instrument.set_mute(self.state < 2)

		# Play the notes
		if self.note_idx < len(self.note_events) and self.note_idx >= 0:
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

class VolumeSlider(GameObject):
	def __init__(self, volume, callback):
		super(VolumeSlider, self).__init__()
		self.volume = volume
		self.callback = callback

		self.outline_sprite = VolumeOutlineSprite()
		self.add_graphic(self.outline_sprite)

		self.volume_graphic = VolumeInsideSprite(volume)
		self.volume_graphic.position = (5, 5)
		self.add_graphic(self.volume_graphic)


		self.position = (120, pattern_height+5)

		self.editing = False

	def on_touch_down(self, event):
		tx, ty = event.touch.pos
		x, y = self.get_abs_pos()
		if y <= ty <= y + volume_slider_size[1]:
			if x <= tx <= x + volume_slider_size[0]:
				self.editing = True
				self.on_touch_move(event)

	def on_touch_move(self, event):
		if not self.editing:
			return
		tx, ty = event.touch.pos
		x, y = self.get_abs_pos()
		self.volume = min(1, max((tx - x - 5) / (volume_slider_size[0]-10), 0))
		self.volume_graphic.set_volume(self.volume)
		self.callback(self.volume)
	def on_touch_up(self, event):
		self.editing = False



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
		else:
			# Instrument button
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








