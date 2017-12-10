from game import GameObject
from components.sprites import *
from common.gfxutil import KFAnim
from kivy.graphics.context_instructions import Color

from virtuals.track import VirtualTrack, VirtualGem, VirtualLane

# Should really fix this graphically and not here.
OFFSET = 2

class Gem(VirtualGem):
	def __init__(self, time, time_quant, seconds, lane_ratio):
		super(Gem, self).__init__(time, time_quant, seconds)
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



	def set_pos(self):
		self.y = self.lane.track.time2y(self.time)
		self.position = (0, self.y-self.sprite.size[1])
		# print self.position.y

	def on_release(self, time):
		super(Gem, self).on_release(time)
		# Draw gradient gem
		if not self.lane.track.drum:
			self.remove_graphic(self.sprite)
			self.sprite = GradientGemSprite(self.sprite.size, self.color, self.sprite.color.rgb)
			self.add_graphic(self.sprite)

	# Called when the gem has been matched -- increase stage count and change color
	# def matched(self, prev_stage):
	# 	self.stage = min(2, prev_stage + 1)
	# 	color = self.color_stages[self.stage]
	# 	self.remove_graphic(self.sprite)
	# 	self.sprite = GemSprite(color)
	# 	self.add_graphic(self.sprite)

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
		# Fade Color
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

class Lane(VirtualLane):
	Gem = Gem
	def __init__(self, count):
		super(Lane, self).__init__(count)
		self.sprite = LaneLineSprite()
		# cx, cy = self.sprite.center
		# self.sprite.center = (cx)
		self.active_gem = None
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
		# self.stage = 0

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

	def on_press(self, time):
		super(Lane, self).on_press(time)
		if self.active_gem:
			self.active_gem.set_pos()

		# check if old gem is already there
		# for gem in self.old_gems:
		# 	if time_quant == gem.time:
		# 		self.match_gem(self.active_gem, gem)
		# 		break


	# def match_gem(self, new_gem, old_gem):
	# 	# print 'matched!'
	# 	new_gem.matched(old_gem.stage)
	# 	self.matching_gem = new_gem

	def remove_old_gems(self):
		to_remove = []
		for gem in self.old_gems:

			if gem.position.y > self.track.now_bar.position[1]:
				# Remove gem entirely
				to_remove.append(gem)

				# Tell the active pattern to remove the note
				if self.track.active:
					self.track.active_pattern.remove_note(gem.time, self.count) #count==lane num

			elif gem.y > self.track.now_bar.position[1]:
				# Set gem length to right length
				gem.update_remove_length(self.track.now_bar.position[1])

		for gem in to_remove:
			self.old_gems.remove(gem)
			self.remove(gem)

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
			# Tell the active pattern to remove the note
			if self.track.active:
				self.track.active_pattern.remove_note(gem.time, self.count) #count==lane num

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
		if self.active_gem is not None:
			self.active_gem.update_length(self.track.now_bar.position[1])
		super(Lane, self).on_lane_update()

class Track(VirtualTrack):
	Lane = Lane
	def __init__(self, num_lanes, bars, tempo, percussive=False):
		super(Track, self).__init__(num_lanes, bars, tempo, percussive)
		self.sprite = TrackSprite()
		self.now_bar = NowBarSprite()
		self.w, self.h = track_size
		self.last_y = 0

		# Dictates whether the player is currently editing a track
		self.set_active(False)

		self.drum = percussive
		# w, h = self.sprite.size

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

		self.add_graphic(self.sprite)
		self.add(*self.lanes)

		self.add_graphic(self.now_bar)

	@property
	def player(self):
		return self._parent

	def set_active(self, active):
		super(Track, self).set_active(active)
		self.sprite.color.rgb = (.3,.8,.7) if active else (.6, .6, .6)
		self.now_bar.color.rgb = now_bar_color if active else (.6, .6, .6)
		if not active:
			if self.player is not None:
				self.player.session.IM.metro.stop()
		else:
			if self.player is not None:
				self.player.session.IM.metro.start()

	def t2y_conversion(self, time):
		return self.sprite.height-self.t2y

	def time2y(self, t):
		return self.h-self.t2y*(t)

	def y2time(self, y):
		return (y+self.h)/(self.t2y*(t%self.seconds))

	def on_update(self): 
		# Display the bar
		self.now_bar.color.rgb = (.13, .54, .13) if self.player.composing else (.7, .7, .7)
		x, _ = self.now_bar.position
		y = self.time2y(self.now)
		self.now_bar.position = (x, y)
		super(Track, self).on_update()
