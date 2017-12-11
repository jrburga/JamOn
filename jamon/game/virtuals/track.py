from jamon.game.game import GameObject
from jamon.game.quantizer import Quantizer

class VirtualGem(GameObject):
	def __init__(self, time, time_quant, seconds, lane_ratio=None):
		super(VirtualGem, self).__init__()
		self.time = time_quant
		self.length = 0
		self.seconds = seconds

	@property
	def lane(self):
		return self._parent

	def on_release(self, time):
		
		if self.lane:
			self.length = time-self.time
			self.lane.track.quant.quantize_gem(self)

	def set_pos_and_size(self):
		pass

	def __repr__(self):
		return '<GEM: %.02f, %.02f>' % (self.time, self.length)

class VirtualLane(GameObject):
	Gem = VirtualGem
	def __init__(self, count):
		super(VirtualLane, self).__init__()
		self.count = count
		self.active_gem = None
		self.current_gems = []
		self.old_gems = []

		self.now = 0

		self.posted_note = False

	@property
	def gems(self):
		return self._game_objects

	@property
	def track(self):
		return self._parent

	def on_press(self, time):
		time_quant = self.track.quant.quantize_note(time)

		if time_quant == self.track.seconds:
			self.posted_note = True
			self.active_gem = None
			return

		for gem in self.current_gems:
			if time_quant == gem.time:
				return

		lane_ratio = float(self.count)/self.track.num_lanes
		gem = self.Gem(time, time_quant, self.track.seconds, lane_ratio)
		self.add(gem)
		self.current_gems.append(gem)
		self.active_gem = gem

	def on_release(self, time):
		if self.active_gem is None:
			return
		self.active_gem.on_release(time)

		if self.track.active:
			pattern = self.track.active_pattern
			pattern.add_note(self.active_gem.time, self.active_gem.length, self.count)

		self.active_gem = None

	# Totally clear the lane
	def refresh(self):
		gems = set(self.gems)
		for gem in gems:
			self.remove(gem)
		self.current_gems = []
		self.old_gems = []
		self.active_gems = None
		self.posted_note = False

	def set_now(self, time):
		self.now = time

	def new_phrase(self):
		for gem in self.old_gems:
			self.remove(gem)
			if self.track.active:
				self.track.active_pattern.remove_note(gem.time, self.count)

		self.old_gems = self.current_gems
		self.current_gems = []

		# release active gems
		if self.active_gem is not None:
			self.on_release(self.track.seconds)

		if self.posted_note:
			self.posted_note = False
			self.on_press(0)

	def remove_old_gems(self):
		to_remove = []
		for gem in self.old_gems:
			if gem.time < self.now:
				to_remove.append(gem)

				if self.track.active:
					self.track.active_pattern.remove_note(gem.time, self.count)

			# elif gem.time > self.now:
			# 	gem.update_remove_length(self.now)

		for gem in to_remove:
			self.old_gems.remove(gem)
			self.remove(gem)

	def on_lane_update(self):
		self.remove_old_gems()

class VirtualTrack(GameObject):
	Lane = VirtualLane
	def __init__(self, num_lanes, bars, tempo, percussive=False):
		super(VirtualTrack, self).__init__()
		self.num_lanes = num_lanes
		self.lanes = [self.Lane(i) for i in range(num_lanes)]
		self.add(*self.lanes)

		self.spb = 60./tempo
		beats = bars*4
		self.seconds = self.spb*beats

		self.now = 0
		self.last_time = 0
		self._active_pattern = None

		self.active = False
		# Add quantizer instance for quantization
		self.quant = Quantizer(self.seconds, bars*8)

	def update_lanes(self, num_lanes):
		self.remove(*self.lanes)
		self.num_lanes = num_lanes
		self.lanes = [self.Lane(i) for i in range(num_lanes)]
		self.add(*self.lanes)

	@property
	def editor(self):
		return self._parent

	@property
	def active_pattern(self):
		return self.editor.active_pattern

	@active_pattern.setter
	def active_pattern(self, active_pattern):
		if self.editor:
			self.editor.active_pattern = active_pattern
		else:
			self._active_pattern = active_pattern

	@property
	def gems(self):
		gems = []
		for lane in self.lanes:
			gems += lane.gems
		return gems

	def on_press(self, lane_num):
		if self.active and lane_num < len(self.lanes):
			self.lanes[lane_num].on_press(self.now)

	def on_release(self, lane_num):
		if self.active and lane_num < len(self.lanes):
			self.lanes[lane_num].on_release(self.now)

	def set_now(self, time):
		for lane in self.lanes:
			lane.set_now(time)
		self.now = time

	def set_active(self, active):
		self.active = active
		if not active:
			self.active_pattern = None
			# remove all gems
			for lane in self.lanes:
				lane.refresh()

	def on_update(self):

		new_phrase = self.last_time > self.now
		self.last_time = self.now

		for lane in self.lanes:
			if new_phrase:
				lane.new_phrase()
			lane.on_lane_update()

		if new_phrase and self.active:
			self.active_pattern.new_phrase()