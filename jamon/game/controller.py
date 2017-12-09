from game import GameObject
from collections import defaultdict

class Controller(GameObject):
	def __init__(self, keys=[]):
		super(Controller, self).__init__()
		self.keys = [key for key in keys]

	def key_down(self, key_index):
		pass

	def key_up(self, key_index):
		pass

class Keyboard(Controller):
	'''
	Directly binds specific keys to actions.
	'''
	def __init__(self, keys=[]):
		super(Keyboard, self).__init__()
		self.keys = [key for key in keys]

	def on_key_down(self, event):
		key = event.keycode[0]
		if key in self.keys:
			index = self.keys.index(key)
			self._parent.key_down(index)

	def on_key_up(self, event):
		key = event.keycode[0]
		if key in self.keys:
			index = self.keys.index(key)
			self._parent.key_up(index)
		elif key == 32: #spacebar
			self._parent.space_bar_pressed()

class NetworkController(Controller):
	def __init__(self, network):
		super(Network, self).__init__()
