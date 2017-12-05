from game import GameObject
from common.synth import Synth
from common.metro import Metronome

class InstrumentManager(GameObject):

	def __init__(self, sched):
		super(InstrumentManager, self).__init__()
		self.synth = Synth("data/FluidR3_GM.sf2")
		self.add_generator(self.synth)

		self.metro = Metronome(sched, self.synth)
		self.inst_count = 1

		self.instruments = []


	# Adds instrument to manager. Each instrument is added to 
	# a new channel.
	def add(self, ins):
		self.inst_count += 1
		self.instruments.append(ins)
		ins.manager = self
		ins.channel = self.inst_count
		self.synth.program(self.inst_count, *ins.patch)

	def noteon(self, *args):
		self.synth.noteon(*args)

	def noteoff(self, *args):
		self.synth.noteoff(*args)



INSTRUMENTS = {
			'piano': ( (  0, 0), [60, 62, 64, 65, 67, 69, 71, 72] ),
			'vibraphone': ( (  0, 11), [60, 62, 64, 65, 67, 69, 71, 72] ),
			'guitar': ( (  0, 24), [48, 50, 52, 53, 55, 57, 59, 60] ),
			'drums': ( (128, 0), [35, 38, 42, 46, 41, 43, 51, 49] )
		}

class Instrument(object):
	
	def __init__(self, inst):
		super(Instrument, self).__init__()
		(self.patch, self.notes) = INSTRUMENTS[inst]
		self.vel = 75
		self.manager = None

	def note_on(self, lane):
		assert 0 <= lane < len(self.notes)
		if self.manager is None:
			print "instrument not added to manager"
			raise Exception
		pitch = self.notes[lane]
		self.manager.noteon(self.channel, pitch, self.vel)


	def note_off(self, lane):
		assert 0 <= lane < len(self.notes)
		if self.manager is None:
			print "instrument not added to manager"
			raise Exception
		pitch = self.notes[lane]
		self.manager.noteoff(self.channel, pitch)
