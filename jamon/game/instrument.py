from game import GameObject
from common.synth import Synth
from common.metro import Metronome
from collections import OrderedDict

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

	def program(self, ins):
		self.synth.program(ins.channel, *ins.patch)

	def noteon(self, *args):
		self.synth.noteon(*args)

	def noteoff(self, *args):
		self.synth.noteoff(*args)



INSTRUMENT_SETS = OrderedDict([
				('ROCK', {'piano': ( (  0, 0), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'vibraphone': ( (  0, 11), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'guitar': ( (  0, 24), [48, 50, 52, 53, 55, 57, 59, 60, 62, 64] ),
					'drum': ( (128, 0), [35, 38, 42, 46, 41, 43, 51, 49] )
				}), 
				('ROCK2', {
					'bass': ( (  0, 33), [36, 38, 40, 41, 43, 45, 47, 48] ),
					'vibraphone': ( (  0, 11), [60, 62, 64, 65, 67, 69, 71, 72] ),
					'guitar': ( (  0, 24), [48, 50, 52, 53, 55, 57, 59, 60] ),
					'drum': ( (128, 0), [35, 38, 42, 46, 41, 43, 51, 49] )
				})])

class Instrument(object):
	
	def __init__(self, inst, inst_set='ROCK'):
		super(Instrument, self).__init__()
		print 'creating instrument:', inst, inst_set
		(self.patch, self.notes) = INSTRUMENT_SETS[inst_set][inst]
		self.vel = 75
		self.inst_set = inst_set
		self.manager = None
		self.mute = False

	def set_inst(self, inst, inst_set=None):
		if inst_set is None:
			inst_set = self.inst_set
		(self.patch, self.notes) = INSTRUMENT_SETS[inst_set][inst]
		self.manager.program(self)

	def note_on(self, lane):
		assert 0 <= lane < len(self.notes)
		if self.manager is None:
			print "instrument not added to manager"
			raise Exception
		pitch = self.notes[lane]
		self.manager.noteon(self.channel, pitch, self.vel if not self.mute else 0)


	def note_off(self, lane):
		assert 0 <= lane < len(self.notes)
		if self.manager is None:
			print "instrument not added to manager"
			raise Exception
		pitch = self.notes[lane]
		self.manager.noteoff(self.channel, pitch)

	def set_mute(self, mute):
		self.mute = mute

