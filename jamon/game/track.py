from game import GameObject
from components.sprites import *
from quantizer import Quantizer

# Should really fix this graphically and not here.
OFFSET = 7

class Track(GameObject):
	def __init__(self, num_lanes, bars, tempo, percussive=False):
		super(Track, self).__init__()
		self.lanes = [Lane() for i in range(num_lanes)]
		self.now = 0
		self.sprite = TrackSprite()
		self.now_bar = NowBarSprite()
		self.w, self.h = self.sprite.size
		self.last_y = 0


		self.drum = percussive
		# w, h = self.sprite.size

		self.spb = 60./tempo
		beats = bars*4
		self.seconds = self.spb*beats

		# Add quantizer instance for quantization
		self.quant = Quantizer(self.seconds, 16)

		self.t2y = self.h/self.seconds
		# self.scale.x = 0.5
		# self.position = ((Window.width-self.w)/2, 0)

		i2lane = self.w/num_lanes
		for i, lane in enumerate(self.lanes):
			lane.position.x = i*i2lane+OFFSET

		self.tempo = tempo
		self.bars = bars

		# self.t2y_ratio = 

		self.add_graphic(self.sprite)
		self.add(*self.lanes)

		#Draw bar lines
		bar_lines = [BarLineSprite(i) for i in range(16)]
		for i, bl in enumerate(bar_lines):
			bl.position = (0, self.h*(1-i/16.)-bl.size[1])
			self.add_graphic(bl)


		self.add_graphic(self.now_bar)

	@property
	def gems(self):
		gems = []
		for lane in self.lanes:
			gems += lane.gems
		return gems

	def lock_in(self):
		for lane in self.lanes:
			lane.lock_in()

	def t2y_conversion(self, time):
		return self.sprite.height-self.t2y

	# def time2y(self, time):
	def on_press(self, lane_num):
		self.lanes[lane_num].on_press(self.now)

	def on_release(self, lane_num):
		self.lanes[lane_num].on_release(self.now)

	def time2y(self, t):
		return self.h-self.t2y*(t)

	def y2time(self, y):
		return (y+self.h)/(self.t2y*(t%self.seconds))

	def set_now(self, time):
		for lane in self.lanes:
			lane.set_now(time)
		self.now = time

	def on_update(self):
		x, _ = self.now_bar.position
		y = self.time2y(self.now)
		self.now_bar.position = (x, y)
		new_phrase = self.last_y < y
		self.last_y = y
		for lane in self.lanes:
			if new_phrase:
				lane.new_phrase()
			lane.on_update()


class Lane(GameObject):
	def __init__(self):
		super(Lane, self).__init__()
		self.sprite = LaneSprite()
		cx, cy = self.sprite.center
		# self.sprite.center = (cx)
		self.active_gem = None
		self.current_gems = []
		self.old_gems = []
		self.locked_gems = []
		# kind of redundant since all game_objets
		# owned by a lane will be gems
		# but maybe not since _game_objects is a set()
		self.now = 0
		w, h = self.sprite.size
		self.add_graphic(self.sprite)


	@property
	def gems(self):
		return self._game_objects

	@property
	def track(self):
		return self._parent

	def lock_in(self):
		# clearing it is definitely buggy. 
		# Fix for later
		
		self.locked_gems = self.current_gems+self.old_gems
		self.old_gems = []
		self.current_gems = []
		for gem in self.locked_gems:
			gem.sprite.color.s = 1.0

	def on_hit(self):
		pass

	def on_pass(self):
		pass

	def on_press(self, time):
		# check if gem is already there
		for gem in self.gems:
			print gem
		gem = Gem((0, 1, 0), time)
		self.add(gem)
		gem.set_pos()
		self.active_gem = gem
		self.current_gems.append(gem)


	def on_release(self, time):
		if self.active_gem is None:
			return
		self.active_gem.length = time-self.active_gem.time
		print self.active_gem.time, self.active_gem.length
		self.active_gem.sprite.color.s = 0.3
		# Quantize gem
		if self.track.drum:
			self.track.quant.quantize_drum_gem(self.active_gem)
		else:
			self.track.quant.quantize_gem(self.active_gem)
		self.active_gem = None

	def remove_old_gems(self):
		to_remove = []
		for gem in self.old_gems:
			if gem.y-gem.get_height() > self.track.now_bar.position[1]:
				to_remove.append(gem)
		for gem in to_remove:
			self.old_gems.remove(gem)
			self.remove(gem)

	def set_now(self, time):
		self.now = time

	def new_phrase(self):
		#Remove any old gems that haven't been removed yet
		for gem in self.old_gems:
			self.remove(gem)
		self.old_gems = self.current_gems
		self.current_gems = []

		# Release active gem, unless the gem was started recently, in which case the player 
		# probably hit it too early while trying to make it start in the first measure.
		if self.active_gem is not None:
			start_thresh = 0.5 #beats
			if self.track.seconds - self.active_gem.time < start_thresh * self.track.spb:
				# Note was made too recently to be released at the end. Change start time to 0
				self.active_gem.time = 0
				self.active_gem.set_pos()
				self.current_gems.append(self.active_gem)
				self.old_gems.remove(self.active_gem)
			else:
				# Release the note
				self.on_release(self.track.seconds)

	def on_update(self):
		if self.active_gem is not None and not self.track.drum:
			self.active_gem.update_length(self.track.now_bar.position[1])
		self.remove_old_gems()
		
class Gem(GameObject):
	def __init__(self, color, time=0, length=0):
		super(Gem, self).__init__()
		self.time = time
		self.length = length
		self.sprite = GemSprite(color)
		self.posistion = (100,100)
		self.add_graphic(self.sprite)
		self.y = 0
		
	@property
	def lane(self):
		return self._parent

	def set_pos(self):
		self.y = self.lane.track.time2y(self.time)
		self.position = (0, self.y)
		# print self.position.y

	def on_hit(self, *args):
		pass

	def on_miss(self, *args):
		pass

	# Function called to render gem based on it's
	# self.time and self.length parameters.
	def set_pos_and_size(self):
		top_y = self.lane.track.time2y(self.time)
		bot_y = self.lane.track.time2y(self.time + self.length)
		size_x, size_y = self.sprite.texture.size
		self.sprite.texture.size = (size_x, top_y - bot_y)
		self.position = (0, bot_y)

	def get_height(self):
		return self.sprite.texture.size[1]

	def update_length(self, y):
		size_x, size_y = self.sprite.texture.size
		self.sprite.texture.size = (size_x, self.y-y)
		self.position.y = y

	def __str__(self):
		return '<GEM %0.2f : %0.2f>' % (self.time, self.length)
