


# The class for all your quantization needs!
class Quantizer:

	# Inputs:
	#	seconds - (float) the total time for one phrase
	#	res     - (int) the number of discrete times per phrase
	#				to discretize to 
	def __init__(self, seconds, res):
		self.seconds = seconds
		self.res = res

		# Seconds per note
		self.spn = seconds / res

	# Given the time of the note, snap to nearest discretized time
	def quantize_note(self, time):
		offset = time % self.spn

		# Check which note is closer
		if offset < self.spn / 2.:
			return time - offset
		else:
			return time - offset + self.spn

	# Performs quantize_note() on the start and end times for the given gem
	def quantize_gem(self, gem):
		new_start = self.quantize_note(gem.time)
		new_end = self.quantize_note(gem.time + gem.length)
		new_length = new_end - new_start
		gem.time = new_start
		gem.length = new_length
		gem.set_pos_and_size()


## Test the class ##
if __name__ == '__main__':
	q = Quantizer(8.0, 16)
	import random
	for i in range(30):
		time = random.random() * 8
		print time, q.quantize_note(time)