from jamon.game.game import GameObject
from components.sprites import *
from kivy.core.window import Window
from widgets import Button
from kivy.core.image import Image
from text import TextObject
from instrument import Instrument

class PatternList(GameObject):

	def __init__(self, bars, tempo):
		super(PatternList, self).__init__()

		self.bars = bars
		self.tempo = tempo

		self.patterns = {}

		self.scroll = ScrollView()
		self.add_btn = PatternButton('add', self.add_btn_clicked)
		self.add_btn.position = (5, pattern_list_height-80)
		self.scroll.add(self.add_btn)
		self.add(self.scroll)

		self.sprite = PatternListSprite()
		self.add_graphic(self.sprite)



	def add_btn_clicked(self):
		# This is for debugging purposes
		print 'add button clicked'
		import random
		self.add_pattern(random.randint(0, 10000000))

	def remove_pattern(self, _id):
		pattern = self.patterns[_id]
		idx = pattern.idx
		self.scroll.remove(pattern)
		del self.patterns[_id]

		# Shift everything below the pattern up
		for k in self.patterns:
			p = self.patterns[k]
			if p.idx > idx:
				p.position.y += pattern_height + spacing

		# Shift add button up
		self.add_btn.position.y += pattern_height + spacing


	def add_pattern(self, _id, seq=[], inst='piano'):
		idx = len(self.patterns)
		pattern = Pattern(_id, idx, self.bars, self.tempo, seq, inst)
		self.scroll.add(pattern)
		self.patterns[_id] = pattern

		# move add button down
		self.add_btn.position.y -= (pattern_height + spacing)

	def set_active(self, pattern):
		self.patterns[pattern].set_active()

	def set_inactive(self, pattern):
		self.patterns[pattern].set_inactive()

	def pattern_editing(self, pattern, editor):
		self.patterns[pattern].editing(editor)

	def pattern_done_editing(self, pattern, seq):
		self.patterns[pattern].done_editing(seq)

	def set_now(self, now):
		for k in self.patterns:
			self.patterns[k].set_now(now)


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




spacing = 50

class Pattern(GameObject):

	def __init__(self, _id, idx, bars, tempo, seq, inst):
		super(Pattern, self).__init__()
		self._id = _id
		self.bars = bars
		self.tempo = tempo
		self.seq = seq
		self.figure_notes()
		self.note_idx = 0
		self.last_time = 0
		self.idx = idx
		self.instrument = Instrument(inst)
		self.num_lanes = len(self.instrument.notes)

		self.now = 0
		self.spb = 60./tempo
		beats = bars*4
		self.seconds = self.spb*beats

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
		self.display_midi()

		# Display pattern buttons
		self.play_btn = PatternButton('play', self.on_play_click)
		self.add(self.play_btn)
		self.delete_btn = PatternButton('delete', self.on_delete_click)
		self.delete_btn.position.x += 30
		self.add(self.delete_btn)

		self.active = False

		self.locked = False

		self.info_text = None

		self.sprites_to_remove = []
		self.objects_to_remove = []

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
		self.notes = []
		for time in sorted(note_dict.iterkeys()):
			self.notes.append( (time, note_dict[time]) )


	def display_midi(self):
		self.note_sprites = []
		for (lane, start, length) in self.seq:
			size_x = pattern_size[0] / self.seconds * length
			size_y = pattern_size[1] / self.num_lanes - 2
			sprite = PatternNoteSprite( (size_x, size_y) )
			sprite.position = (start * pattern_size[0] / self.seconds, lane * pattern_size[1] / self.num_lanes)
			self.note_sprites.append(sprite)
			self.add_graphic(sprite)

	def on_play_click(self):
		if self.locked:
			return
		print '%d clicked' % self._id

	def on_delete_click(self):
		if self.locked:
			return
		# This is for degubbing purposes
		self._parent._parent.remove_pattern(self._id)

	def set_active(self):
		if self.active:
			return
		self.active = True
		self.outline_sprite.color.v = 1
		self.outline_sprite.color.h = 0.9

	def set_inactive(self):
		if not self.active:
			return
		self.active = False
		self.outline_sprite.color.v = 0.5
		self.outline_sprite.color.h = 0.55

	def toggle_active(self):
		if self.active:
			self.set_inactive()
		else:
			self.set_active()

	def editing(self, editor):
		self.locked = True
		self.outline_sprite.color.v = 1
		self.outline_sprite.color.h = 0

		if self.info_text is not None:
			self.objects_to_remove.append(self.info_text)
		self.info_text = TextObject(editor+' is editing...', font_size=14, color=self.outline_sprite.color.rgb)
		self.info_text.position = (70, pattern_height)
		self.add(self.info_text)

	def done_editing(self, seq):
		self.seq = seq
		for ns in self.note_sprites:
			self.sprites_to_remove.append(ns)
		self.display_midi()
		self.locked = False
		if self.info_text is not None:
			self.objects_to_remove.append(self.info_text)
		self.active = False
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

		# Play the notes
		if self.now < self.last_time:
			self.note_idx = 0
		if self.note_idx < len(self.notes):
			time, events = self.notes[self.note_idx]
			if self.now > time:
				self.note_idx += 1
				for (onoff, lane) in events:
					if onoff == 'on':
						print 'on', time, lane
						self.instrument.note_on(lane)
					else:
						self.instrument.note_off(lane)
						print 'off', time, lane
		self.last_time = self.now



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

		self.sprite.position = (5, pattern_height)
		self.sprite.color.v = 0.5
		self.add_graphic(self.sprite)

		self.events = []


	def on_touch_down(self, event):
		x, y = event.touch.pos
		self.figure_pos()
		if abs(x - self.x) < 15 and abs(y - self.y) < 15:
			self.touched = True
			self.sprite.color.v = 1

	def on_touch_up(self, event):
		if self.touched:
			self.touched = False
			self.events.append(self.callback)
			self.sprite.color.v = 0.5


	def figure_pos(self):
		x, y = self.get_abs_pos()
		x += 20
		y += pattern_height + 15
		self.x = x
		self.y = y

	def on_update(self):
		while self.events:
			self.events.pop(0)()








