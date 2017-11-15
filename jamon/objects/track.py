from ..game import GameObject

class Track(GameObject):
	def __init__(self):
		super(Track, self).__init__()
		self.now_bar = None
		self.lanes = {}
