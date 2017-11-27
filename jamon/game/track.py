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
		self.quant = Quantizer(self.seconds, 32)

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

	@property
	def player(self):
		return self._parent

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
		

		# Display the bar
		self.now_bar.color.rgb = (.13, .54, .13) if self.player.composing else (.7, .7, .7)

		x, _ = self.now_bar.position
		y = self.time2y(self.now)
		self.now_bar.position = (x, y)
		new_phrase = self.last_y < y
		self.last_y = y

		if not self.player.composing:
			return

		for lane in self.lanes:
			if new_phrase:
				lane.new_phrase()
			lane.on_lane_update()

		if new_phrase:
			notes_entered = False
			all_locked = True
			for lane in self.lanes:
				stage = lane.stage
				notes_entered = notes_entered or stage > 0
				if stage > 0:
					all_locked = all_locked and stage == 3

			if notes_entered and all_locked:
				print "TRACK LOCKED IN"
				self.player.lock_in_sequence()


class Lane(GameObject):
	COUNT = 0
	def __init__(self):
		super(Lane, self).__init__()
		self.count = Lane.COUNT
		Lane.COUNT += 1
		self.sprite = LaneSprite()
		cx, cy = self.sprite.center
		# self.sprite.center = (cx)
		self.active_gem = None
		self.poss_gem = None
		self.current_gems = []
		self.old_gems = []
		self.locked_times = []
		self.prev_num_locked = 0
		# kind of redundant since all game_objets
		# owned by a lane will be gems
		# but maybe not since _game_objects is a set()
		self.now = 0
		w, h = self.sprite.size
		self.add_graphic(self.sprite)

		# Represents how locked in the lane is
		# 0 - no notes
		# 1 - still inserting notes
		# 2 - all noted locked in but repeating one more time
		# 3 - lane locked
		# Updated at end of every phrase
		self.stage = 0

		self.posted_note = False


	@property
	def gems(self):
		return self._game_objects

	@property
	def track(self):
		return self._parent

	def on_hit(self):
		pass

	def on_pass(self):
		pass

	def on_press(self, time):
		time_quant = self.track.quant.quantize_note(time)

		# Note will appear on start of next round
		if time_quant == self.track.seconds:
			print 'posting note'
			self.posted_note = True
			self.active_gem = None
			return

		# check if current gem is already there
		for gem in self.current_gems:
			# Don't make a new gem if there is already a gem within
			# the same beat grid (dictated from Quantizer)
			if time_quant == gem.time:
				print 'gem overlap'
				return

		# check if old gem is already there
		for gem in self.old_gems:
			if time_quant == gem.time:
				#Save gem for beatmatching possiblity
				self.poss_gem = gem
				break
		gem = Gem(0, time_quant)
		self.add(gem)
		gem.set_pos()
		self.active_gem = gem
		self.current_gems.append(gem)


	def on_release(self, time):
		if self.active_gem is None:
			return
		self.active_gem.on_release(time)
		# Check if beat matched:
		if self.poss_gem is not None:
			if self.track.drum or self.active_gem.length == self.poss_gem.length:
				print 'matched!'
				self.active_gem.matched(self.poss_gem.stage)
				# Check if gem is in final stage (locked in)
				if self.active_gem.stage >= 1:
					if (self.active_gem.time, self.active_gem.length) not in self.locked_times:
						self.locked_times.append( (self.active_gem.time, self.active_gem.length) )
					print 'Gem locked in'
		self.poss_gem = None
		self.active_gem = None

	def remove_old_gems(self):
		to_remove = []
		for gem in self.old_gems:
			if gem.y-gem.get_height() > self.track.now_bar.position[1]:
				print 'removing gem'
				to_remove.append(gem)
		for gem in to_remove:
			self.old_gems.remove(gem)
			self.remove(gem)

	def set_now(self, time):
		self.now = time

	def new_phrase(self):
		#Remove any old gems that haven't been removed yet
		
		num_curr = len(self.current_gems)
		for gem in self.old_gems:
			self.remove(gem)
		self.old_gems = self.current_gems
		self.current_gems = []

		# Release active gem
		if self.active_gem is not None:
			self.on_release(self.track.seconds)
		

		print "CURRENT GEMS:", num_curr
		print "LOCKED TIMES:", len(self.locked_times)
		print "PREV LOCKED:", self.prev_num_locked
		# Figure new stage
		if self.stage == 0:
			if num_curr > 0:
				self.stage = 1
		elif self.stage == 1:
			if num_curr == 0:
				self.stage = 0
			elif num_curr == len(self.locked_times):
				self.stage = 2
		elif self.stage == 2:
			if num_curr == 0:
				self.stage = 0
			elif num_curr == len(self.locked_times) == self.prev_num_locked:
				self.stage = 3
			else:
				self.stage = 2

		print 'new stage:', self.stage

		if self.stage == 3:
			return

		self.prev_num_locked = len(self.locked_times)
		self.locked_times = []


		if self.posted_note:
			# Post note at beginning of loop
			self.posted_note = False
			self.on_press(0)

	def on_lane_update(self):
		if self.active_gem is not None and not self.track.drum:
			self.active_gem.update_length(self.track.now_bar.position[1])
		self.remove_old_gems()
		
class Gem(GameObject):
	def __init__(self, stage=0, time=0, length=0):
		super(Gem, self).__init__()
		self.time = time
		self.length = length
		self.stage = stage
		self.color_stages = ((.8, .3, .4), (.5, .55, .4), (.2, .8, .4))
		color = self.color_stages[stage]
		self.sprite = GemSprite(color)
		self.posistion = (100,100)
		self.add_graphic(self.sprite)
		self.y = 0

		
		
	@property
	def lane(self):
		return self._parent

	def set_pos(self):
		self.y = self.lane.track.time2y(self.time)
		self.position = (0, self.y-self.sprite.size[1])
		# print self.position.y

	def on_hit(self, *args):
		pass

	def on_miss(self, *args):
		pass

	def on_release(self, time):
		self.length = time-self.time
		# Quantize gem
		if self.lane.track.drum:
			self.lane.track.quant.quantize_drum_gem(self)
		else:
			self.lane.track.quant.quantize_gem(self)

		# Draw gradient gem
		self.add_graphic(GradientGemSprite(self.sprite.size, self.color_stages[0]))

	# Called when the gem has been matched -- increase stage count and change color
	def matched(self, prev_stage):
		self.stage = min(2, prev_stage + 1)
		color = self.color_stages[self.stage]
		# Dispay gradient if not drum note
		if not self.lane.track.drum:
			self.add_graphic(GradientGemSprite(self.sprite.size, color))
		else:
			#Just change color
			self.add_graphic(GemSprite(color))

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
