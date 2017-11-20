from game import GameObject
from common.fluidsynth import Synth

class Instrument(GameObject):
	def __init__(self):
		super(Instrument, self).__init__()
		self.notes = []

		# self.add_generator()

	def note_on(self, note):
		# should play not at note index or something
		pass

	def note_off(self, note):
		# 
		pass