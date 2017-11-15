from ..game import GameObject

from collections import defaultdict

class Controller(GameObject):
	def __init__(self):
		super(Controller, self).__init__()
		self.keys = defaultdict(lambda : False)

	def get_pressed(self):
		return [i for i in self.inputs if self.inputs[i] == True]

	def set_pressed(self, i, pressed):
		self.keys[i] = True

class Keyboard(Controller):
	def __init__(self):
		super(Keyboard, self).__init__()

	def on_key_down(self, event):
		self.keys[event.keycode[0]] = True
		
	def on_key_up(self, event):
		self.keys[event.keycode[0]] = False