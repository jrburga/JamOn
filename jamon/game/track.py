from game import GameObject
from components.sprites import *
from quantizer import Quantizer
from common.gfxutil import KFAnim
from kivy.graphics.context_instructions import Color

# Should really fix this graphically and not here.
OFFSET = 2

class Track(GameObject):
	def __init__(self, num_lanes, bars, tempo, percussive=False):
		super(Track, self).__init__()
		self.lanes = [Lane() for i in range(num_lanes)]
		self.now = 0
		self.sprite = TrackSprite()
		self.now_bar = NowBarSprite()
		self.w, self.h = track_size
		self.last_y = 0
		self.num_lanes = num_lanes


		self.drum = percussive
		# w, h = self.sprite.size

		self.spb = 60./tempo
		beats = bars*4
		self.seconds = self.spb*beats

		# Add quantizer instance for quantization
		self.quant = Quantizer(self.seconds, bars*8)

		self.t2y = self.h/self.seconds
		# self.scale.x = 0.5
		# self.position = ((Window.width-self.w)/2, 0)

		# Draw bar lines
		bar_lines = [BarLineSprite(i) for i in range(16)]
		for i, bl in enumerate(bar_lines):
			bl.position = (0, self.h*(1-i/16.)-bl.size[1])
			self.add_graphic(bl)

		i2lane = self.w/num_lanes
		for i, lane in enumerate(self.lanes):
			lane.position.x = i*i2lane+OFFSET
			lane.scale.x = 1. / (num_lanes+1)

		self.tempo = tempo
		self.bars = bars

		self.num_lanes = num_lanes

		# self.t2y_ratio = 

		# self.add_graphic(self.sprite)
		self.add(*self.lanes)

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
					all_locked = all_locked and stage == 2

			if notes_entered and all_locked:
				print "TRACK LOCKED IN"
				self.player.lock_in_sequence()


class Lane(GameObject):
	COUNT = 0
	def __init__(self):
		super(Lane, self).__init__()
		self.count = Lane.COUNT
		Lane.COUNT += 1
		self.sprite = LaneLineSprite()
		# cx, cy = self.sprite.center
		# self.sprite.center = (cx)
		self.active_gem = None
		self.matching_gem = None
		self.current_gems = []
		self.old_gems = []
		# kind of redundant since all game_objets
		# owned by a lane will be gems
		# but maybe not since _game_objects is a set()
		self.now = 0
		w, h = lane_size
		self.add_graphic(self.sprite)
		

		# Represents how locked in the lane is
		# 0 - no notes
		# 1 - still inserting notes
		# 2 - all locked
		# Updated at end of every phrase
		self.stage = 0

		self.posted_note = False

		# # Draw bar lines
		# bar_lines = [BarLineSprite(i) for i in range(16)]
		# for i, bl in enumerate(bar_lines):
		# 	bl.position = (0, h*(1-i/16.)-bl.size[1])
		# 	self.add_graphic(bl)

	def on_add(self):
		if self.count == self.track.num_lanes - 1:
			secondLine = LaneLineSprite()
			secondLine.position = (lane_width+5, 0)
			self.add_graphic(secondLine)


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
			self.posted_note = True
			self.active_gem = None
			return

		# check if current gem is already there
		for gem in self.current_gems:
			# Don't make a new gem if there is already a gem within
			# the same beat grid (dictated from Quantizer)
			if time_quant == gem.time:
				return

		gem = Gem(time, time_quant, self.track.seconds, float(self.count)/self.track.num_lanes)
		self.add(gem)
		gem.set_pos()
		self.active_gem = gem
		self.current_gems.append(gem)

		# check if old gem is already there
		# for gem in self.old_gems:
		# 	if time_quant == gem.time:
		# 		self.match_gem(self.active_gem, gem)
		# 		break


	def match_gem(self, new_gem, old_gem):
		# print 'matched!'
		new_gem.matched(old_gem.stage)
		self.matching_gem = new_gem

	def on_release(self, time):
		if self.active_gem is None:
			return
		self.active_gem.on_release(time)

		if self.matching_gem is not None:
				# Finish off the matching
				# Check if gem is in final stage (locked in)
				# if self.matching_gem.stage >= 1:
				# 	if (self.matching_gem.time, self.matching_gem.length) not in self.locked_times:
				# 		self.locked_times.append( (self.matching_gem.time, self.matching_gem.length) )
				#	 print 'Gem locked in'
				pass
		self.matching_gem = None
		self.active_gem = None

	def remove_old_gems(self):
		to_remove = []
		for gem in self.old_gems:

			if gem.position.y > self.track.now_bar.position[1]:
				# Remove gem entirely
				to_remove.append(gem)

			elif gem.y > self.track.now_bar.position[1]:
				# Set gem length to right length
				gem.update_remove_length(self.track.now_bar.position[1])

		for gem in to_remove:
			self.old_gems.remove(gem)
			self.remove(gem)

	def set_now(self, time):
		self.now = time

	def new_phrase(self):
		# stages = [gem.stage for gem in self.current_gems]
		# self.locked_times = [(gem.time, gem.length) for gem in self.current_gems]
		# print 'gem stages:', stages
		# notes_entered = len(stages) > 0
		# all_locked = all(stage==2 for stage in stages)
		# if all_locked:
		# 	print 'all locked'
		
		# Remove lingering old gems
		for gem in self.old_gems:
			self.remove(gem)
		self.old_gems = self.current_gems
		self.current_gems = []

		# Release active gem
		if self.active_gem is not None:
			self.on_release(self.track.seconds)
		
		# Figure new stage
		# if self.stage == 0:
		# 	if notes_entered:
		# 		self.stage = 1
		# elif self.stage == 1:
		# 	if not notes_entered:
		# 		self.stage = 0
		# 	elif all_locked:
		# 		self.stage = 2

		# print 'new stage:', self.stage

		# if self.stage == 2:
		# 	return

		if self.posted_note:
			# Post note at beginning of loop
			self.posted_note = False
			self.on_press(0)

	def on_lane_update(self):
		if self.active_gem is not None and not self.track.drum:
			self.active_gem.update_length(self.track.now_bar.position[1])
		self.remove_old_gems()
		
class Gem(GameObject):
	def __init__(self, time, time_quant, seconds, lane_ratio):
		super(Gem, self).__init__()
		self.time = time_quant
		self.length = 0
		self.seconds = seconds
		# self.color_stages = ((.8, .3, .4), (.85, .75, .1), (.2, .8, .4))
		self.color = Color(0.3+0.7*lane_ratio, 0.8, 1, mode='hsv').rgb
		self.sprite = GemSprite(self.color)
		self.posistion = (100,100)
		self.add_graphic(self.sprite)
		self.y = 0

		self.total_height = None

		# For fading
		self.last_time = time
		self.anim = KFAnim( (0,0.8), (seconds,.3))

		
		
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
		if not self.lane.track.drum:
			self.remove_graphic(self.sprite)
			self.sprite = GradientGemSprite(self.sprite.size, self.color, self.sprite.color.rgb)
			self.add_graphic(self.sprite)

	# Called when the gem has been matched -- increase stage count and change color
	def matched(self, prev_stage):
		self.stage = min(2, prev_stage + 1)
		color = self.color_stages[self.stage]
		self.remove_graphic(self.sprite)
		self.sprite = GemSprite(color)
		self.add_graphic(self.sprite)

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

	def update_remove_length(self, y):
		if self.total_height is None:
			# Rememeber height before shrinking
			self.total_height = self.get_height()
		size_x, size_y = self.sprite.texture.size
		self.sprite.texture.size = (size_x, self.total_height - self.y + y)

	def on_update(self):
		# Fade color
		now = self.lane.now
		dt = now - self.last_time % self.seconds
		if now < self.last_time % self.seconds:
			# New frame
			dt += self.seconds
		s = self.anim.eval(self.last_time-self.time)
		self.sprite.color.v = s
		self.last_time += dt


	def __str__(self):
		return '<GEM %0.2f : %0.2f>' % (self.time, self.length)
