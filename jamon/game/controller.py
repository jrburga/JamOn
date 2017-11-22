from game import GameObject
from collections import defaultdict

class Controller(GameObject):
	def __init__(self, keys):
		super(Controller, self).__init__()
		self.keys = []

	def get_pressed(self):
		return [i for i in self.inputs if self.inputs[i] == True]

	def set_pressed(self, i, press):
		self.keys[i] = press

class Keyboard(Controller):
	'''
	Directly binds specific keys to actions.
	'''
	def __init__(self):
		super(Keyboard, self).__init__([])
		self.keys = []


	def on_key_down(self, event):
		key = event.keycode[0]
		if key in self.keys:
			index = self.keys.index(key)
			self.key_down(index)

	def on_key_up(self, event):
		key = event.keycode[0]
		if key in self.keys:
			index = self.keys.index(key)
			self.key_up(index)

	def key_down(self, key_index):
		pass

	def key_up(self, key_index):
		pass

class Network(Controller):
	def __init__(self):
		super(Controller, self).__init__([])