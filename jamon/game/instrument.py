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


TEMPOS = {'ROCK':110, 'ELECTRO':128, 'JAZZ':125}

INSTRUMENT_SETS = OrderedDict([
				('ROCK', {'piano': ( (  0, 0), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'vibraphone': ( (  0, 11), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'guitar': ( (  0, 24), [48, 50, 52, 53, 55, 57, 59, 60, 62, 64] ),
					'drum': ( (128, 0), [35, 38, 42, 46, 41, 43, 51, 49] ),
					'bass': ( (  0, 33), [33, 35, 36, 38, 40, 41, 43, 45, 47, 48] )
				}), 
				('ELECTRO', {
					'synth': ( (  0, 80), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'trumpet': ( (  0, 62), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'drum': ( (128, 24), [35, 38, 42, 46, 41, 43, 51, 49] ),
					'bass': ( (  0, 38), [33, 35, 36, 38, 40, 41, 43, 45, 47, 48] )
				}),
				('JAZZ', {
					'bass': ( (  0, 32), [36, 38, 40, 41, 43, 45, 47, 48] ),
					'trumpet': ( (  0, 56), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'sax': ( (  0, 65), [60, 62, 64, 65, 67, 69, 71, 72, 74, 76] ),
					'drum': ( (128, 0), [35, 38, 42, 46, 41, 43, 51, 49] ),
					'piano': ( (0,0), [(60,64,67,69),
									(62,65,69,72),
									(64,67,71,74),
									(65,69,72,76),
									(55,65,67,71,74),
									(67,69,72,76),
									(69,71,74,77),
									(60,64,67,71),
									(60,64,66,69),
									])
				})
			])

class Instrument(object):
	
	def __init__(self, inst, inst_set='ROCK'):
		super(Instrument, self).__init__()
		print 'creating instrument:', inst, inst_set
		(self.patch, self.notes) = INSTRUMENT_SETS[inst_set][inst]
		self.vel = 75
		self.inst_set = inst_set
		self.manager = None
		self.mute = False

	def set_volume(self, vol):
		self.vel = int(vol * 100)

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
		pitches = self.notes[lane]
		if type(pitches) != tuple:
			pitches = [pitches]
		for pitch in pitches:
			self.manager.noteon(self.channel, pitch, self.vel if not self.mute else 0)


	def note_off(self, lane):
		assert 0 <= lane < len(self.notes)
		if self.manager is None:
			print "instrument not added to manager"
			raise Exception
		pitches = self.notes[lane]
		if type(pitches) != tuple:
			pitches = [pitches]
		for pitch in pitches:
			self.manager.noteoff(self.channel, pitch)

	def set_mute(self, mute):
		self.mute = mute

