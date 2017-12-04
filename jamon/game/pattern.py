from jamon.game.game import GameObject
from components.sprites import *
from kivy.core.window import Window
from widgets import Button
from kivy.core.image import Image
from text import TextObject

class PatternList(GameObject):

	def __init__(self, bars):
		super(PatternList, self).__init__()

		self.bars = bars

		

		self.patterns = {}

		self.scroll = ScrollView()
		self.add(self.scroll)

		self.sprite = PatternListSprite()
		self.add_graphic(self.sprite)

	def add_pattern(self, _id, seq=[], num_lanes=8):
		idx = len(self.patterns)
		pattern = Pattern(_id, idx, self.bars, seq, num_lanes)
		self.scroll.add(pattern)
		self.patterns[_id] = pattern

	def set_active(self, pattern):
		self.patterns[pattern].set_active()

	def set_inactive(self, pattern):
		self.patterns[pattern].set_inactive()

	def pattern_editing(self, pattern, editor):
		self.patterns[pattern].editing(editor)

	def pattern_done_editing(self, pattern, seq):
		self.patterns[pattern].done_editing(seq)


class ScrollView(GameObject):
	def __init__(self):
		super(ScrollView, self).__init__()
		self.up = False
		self.down = False


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






class Pattern(GameObject):

	def __init__(self, _id, idx, bars, seq, num_lanes):
		super(Pattern, self).__init__()
		self._id = _id
		self.bars = bars
		self.seq = seq
		self.idx = idx
		self.num_lanes = num_lanes

		# Display the pattern outline
		self.outline_sprite = PatternOutlineSprite()
		self.outline_sprite.color.v = 0.5
		self.outline_sprite.color.h = .55
		self.add_graphic(self.outline_sprite)
		spacing = 50
		self.position.x = 5
		self.position.y = pattern_list_height - (pattern_height + spacing) * (1 + idx)

		# Display MIDI
		self.display_midi()

		# Display pattern buttons
		self.play_btn = PatternButton('play', self.on_play_click)
		self.add(self.play_btn)

		self.active = False

		self.locked = False

		self.info_text = None

		self.sprites_to_remove = []
		self.objects_to_remove = []

	def display_midi(self):
		self.note_sprites = []
		for (lane, start, length) in self.seq:
			size_x = pattern_size[0] / self.bars * length / 2 # why is /2 needed here...?
			size_y = pattern_size[1] / self.num_lanes - 2
			sprite = PatternNoteSprite( (size_x, size_y) )
			sprite.position = (start * pattern_size[0] / self.bars / 2, lane * pattern_size[1] / self.num_lanes)
			self.note_sprites.append(sprite)
			self.add_graphic(sprite)

	def on_play_click(self):
		if self.locked:
			return

		print '%d clicked' % self._id


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
		self.info_text.position = (60, pattern_height)
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

	def on_update(self):
		# Needs to be handled synchronously and not from events
		for s in self.sprites_to_remove:
			# I had to do this because of a weird KeyError....
			if s in self._graphics._objects:
				self.remove_graphic(s)
		for o in self.objects_to_remove:
			self.remove(o)

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

		self.sprite.position = (5, pattern_height)
		self.sprite.color.v = 0.5
		self.add_graphic(self.sprite)


	def on_touch_down(self, event):
		x, y = event.touch.pos
		self.figure_pos()
		if abs(x - self.x) < 10 and abs(y - self.y) < 10:
			print 'TOUCHED!'
			self.touched = True
			self.callback()
			self.sprite.color.v = 1

	def on_touch_up(self, event):
		if self.touched:
			self.touched = False
			self.sprite.color.v = 0.5


	def figure_pos(self):
		x, y = self.get_abs_pos()
		x += 15
		y += pattern_height + 10
		print 'POS:', x, y
		self.x = x
		self.y = y







