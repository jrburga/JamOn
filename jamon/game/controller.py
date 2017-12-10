from game import GameObject

from collections import defaultdict

class KeyMapping(dict):
	@property
	def is_empty(self):
		return len(self) != 0

	def __missing__(self, key):
		return None

class VirtualController(GameObject):
	KEYDOWN = 0
	KEYUP = 1
	def __init__(self, vid):
		super(VirtualController, self).__init__()
		self._actions = defaultdict(lambda: {self.KEYDOWN: [],
											 self.KEYUP: []})
		self._vid = vid

	@property
	def vid(self):
		return self._vid

	def bind_keydown(self, vkey, action):
		self._actions[vkey][self.KEYDOWN].append(action)

	def bind_keyup(self, vkey, action):
		self._actions[vkey][self.KEYUP].append(action)

	def on_vkey_down(self, event):
		vkey = event.vkey
		vid = event.vid
		if vid != self.vid: return
		# print 'executing vkey down', vkey, vid
		for action in self._actions[vkey][self.KEYDOWN]:
			action()

	def on_vkey_up(self, event):
		vkey = event.vkey
		vid = event.vid
		if vid != self.vid: return
		for action in self._actions[vkey][self.KEYUP]:
			action()

class InstrumentController(VirtualController):
	def __init__(self, num_notes, vid):
		super(InstrumentController, self).__init__(vid)
		self.num_notes = num_notes

	def bind_lock_in(self, action):
		self._actions[-1][self.KEYDOWN].append(action)

	def bind_notes(self, key_down_cb, key_up_cb):
		for i in xrange(self.num_notes):
			self.bind_keydown(i, key_down_cb(i))
			self.bind_keyup(i, key_up_cb(i))

class InstrumentKeyboard(InstrumentController):
	def __init__(self, note_keycodes, lock_in_keycode):
		super(InstrumentKeyboard, self).__init__(len(note_keycodes), None)
		self._keymapping = KeyMapping({kc: i for i, kc in enumerate(note_keycodes)})
		self._keymapping[lock_in_keycode] = -1
		self._actions = defaultdict(lambda: {self.KEYDOWN: [],
											 self.KEYUP: []})

	@property
	def vid(self):
		return self.client.id if self.client else None

	def on_key_down(self, event):
		vkey = self._keymapping[event.keycode[0]]
		for action in self._actions[vkey][self.KEYDOWN]:
			action()
		if self.client:
			self.client.send_action('on_vkey_down', vkey=vkey, vid=self.vid)

	def on_key_up(self, event):
		vkey = self._keymapping[event.keycode[0]]
		for action in self._actions[vkey][self.KEYUP]:
			action()
		if self.client:
			self.client.send_action('on_vkey_up', vkey=vkey, vid=self.vid)





