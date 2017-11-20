from game import GameObject
from common.fluidsynth import Synth

class InstrumentManager(GameObject):

	def __init__(self):
		super(Instrument, self).__init__()
		self.synth = Synth("../data/FluidR3_GM.sf2")
		self.add_generator(self.synth)
		self.inst_count = 0


	# Adds instrument to manager. Each instrument is added to 
	# a new channel.
	# Inputs:
	#		patch -- tuple of (bank, program)
	# Returns the instrument's channel number
	def add_instrument(self, patch):
		self.inst_count += 1
		self.synth.program(self.inst_count, *patch)
		return self.inst_count

	def noteon(self, *args):
		self.synth.noteon(*args)

	def noteoff(self, *args):
		self.synth.noteoff(*args)


IM = InstrumentManager()


INSTRUMENTS = {
			'piano': ( (0,0), [60, 62, 64, 65, 67, 69, 71, 72] )
		}

class Instrument(object):
	
	def __init__(self, inst):
		super(Instrument, self).__init__()
		(self.patch, self.notes) = INSTRUMENTS[inst]
		self.channel = IM.add_instrument(self.patch)
		self.vel = 75

	def note_on(self, lane):
		pitch = self.notes[lane]
		IM.noteon(self.channel, pitch, self.vel)


	def note_off(self, note):
		pitch = self.notes[lane]
		IM.noteoff(self.channel, pitch)
