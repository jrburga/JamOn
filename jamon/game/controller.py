from game import GameObject
from collections import defaultdict

class Keyboard(GameObject):
	KEYDOWN = 0
	KEYUP = 1
	def __init__(self):
		super(Keyboard, self).__init__()
		self._actions = defaultdict(lambda: {self.KEYDOWN: [],
											 self.KEYUP: []})
	@property
	def bindings(self):
		return self._actions.keys()

	def bind_keydown(self, keycode, action):
		self._actions[keycode][self.KEYDOWN].append(action)

	def bind_keyup(self, keycode, action):
		self._actions[keycode][self.KEYUP].append(action)

	def on_key_down(self, event):
		keycode = event.keycode[0]
		for action in self._actions[keycode][self.KEYDOWN]:
			action()

	def on_key_up(self, event):
		keycode = event.keycode[0]
		for action in self._actions[keycode][self.KEYUP]:
			action()

class QuickKeyboard(Keyboard):
	def __init__(self, keycodes):
		super(QuickKeyboard, self).__init__()
		self.keycodes = keycodes

	def bind_callbacks(self, up_cb, down_cb):
		for i, key in enumerate(self.keycodes):
			self.bind_keydown(key, lambda : self._down_cb(i))
			self.bind_keyup(key, lambda : self._up_cb(i))			

	def set_callbacks(self, down_cb, up_cb):
		self._down_cb = down_cb
		self._up_cb = up_cb

class VirtualController(GameObject):
	def __init__(self, vid):
		super(VirtualController, self).__init__()
		self.vid = vid

	def on_vkey_down(self, event):
		vkey = event.vkey
		vid = event.vid
		if vid != self.id: return
		for action in self._actions[vkey][self.KEYDOWN]:
			action()

	def on_vkey_up(self, event):
		key = event.vkey
		vid = event.vid
		if vid != self.id: return
		for action in self._actions[vkey][self.KEYUP]:
			action()

