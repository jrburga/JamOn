# Scene for when player has clicked join_game and successfully joins

from urllib2 import urlopen
import json

from jamon.game.game import Scene, GameObject
from jamon.game.components.graphics import *
from jamon.game.widgets import *
from jamon.game.text import TextObject
from jamon.game.instrument import INSTRUMENT_SETS

from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.core.window import Window



class WaitingRoom(Scene):
	def __init__(self, **kwargs):
		super(WaitingRoom, self).__init__(**kwargs)
		self.client = self.base_widget.client_obj
		self.add(self.client)
		self.is_host = self.client.is_host
		self.band_members = []
		self.client.post_info('band_members', self.client.info())
		self.client.send_action('on_join')
		self.next_band_member_index = 0


		# REMOVE THIS
		# if self.is_host:
		# 	self.host = self.base_widget.game_state.server_object

		# 	# Trigger host search for other players
		# 	self.host.find_other_players()

		# self.band_members = self.base_widget.game_state.server_object.band_members
		# self.my_ip = urlopen('http://ip.42.pl/raw').read()

		self.general_display()
		self.band_display()

	def on_join(self, event):
		print 'getting band info'

		self.band_members = self.client.get_info('band_members', None)
		print self.band_members
		for i in range(self.next_band_member_index, len(self.band_members)):
			self.make_user_blurb(i, is_me=False)

		self.next_band_member_index = i+1

	def general_display(self):
		"""
		All of the non-player-specific display will be handled here
		"""
		# for start_game, instrument buttons
		self.button_dist_from_side = Window.width/25.0
		self.button_dist_from_top = Window.height * 0.3
		self.button_dist_from_bottom = Window.height/15.0

		# for instrument buttons
		self.button_width = Window.width / 4.0


		# I thinnk we should remove the waiting_room_label cuz why bother keeping it
		# self.waiting_room_label_pos = (Window.width / 15.0, Window.height * 0.8)
		# self.waiting_room_label = TextObject(text="[anchor=left_side][color=ff8888][b]Waiting Room[/b][/color][anchor=right_side]", 
		# 							   font_size=150, markup=True, halign='left', valign='bottom',
		# 							   pos=self.waiting_room_label_pos)

		# self.add_game_object(self.waiting_room_label)

		self.start_game_size = (Window.width * 0.25, Window.height * 0.1)
		self.start_game_button_pos = (self.button_dist_from_side, Window.height - self.start_game_size[1] - self.button_dist_from_bottom)

		if self.is_host:
			# To let host start the game
			self.start_game_button = Button(text=" Let's Jam! ", font_size='50sp', markup=True, 
											halign='center', valign='top',
											pos=self.start_game_button_pos,
											size=self.start_game_size)

			self.start_game_button.bind(self.start_game_callback())
			self.add_game_object(self.start_game_button)

		self.the_band_label_pos = (self.button_dist_from_side + Window.width/50.0, Window.height - self.button_dist_from_top)
		self.the_band_label = TextObject(text="[anchor=left_side][color=ff8888][b]The Band[/b][/color][anchor=right_side]", 
									   font_size=150, markup=True, halign='left', valign='bottom',
									   pos=self.the_band_label_pos)

		self.add_game_object(self.the_band_label)

		if self.is_host:
			# TODO right align the Instruments label
			# self.instruments_label_size = (1000, 1000) #overly large so it doesn't constrain the word
			
			self.instruments_label_pos = (Window.width - self.button_dist_from_side - self.button_width, \
											Window.height - self.button_dist_from_top)
			self.instruments_label = TextObject(text="[color=abcdef][b]Instruments[/b][/color]", 
										   font_size=100, markup=True, valign='bottom', halign='left', #halign='right',
										   pos=self.instruments_label_pos)

			self.add_game_object(self.instruments_label)
			self.make_instrument_buttons()

	def make_instrument_buttons(self):
		"""
		Makes the buttons for the instrument sets
		"""
		# Constants
		dist_between_buttons = Window.height/50.0

		num_sets = len(INSTRUMENT_SETS)
		i = 0
		button_height = (Window.height - (self.button_dist_from_top + self.button_dist_from_bottom)) / num_sets - dist_between_buttons
		button_x = Window.width - self.button_width - self.button_dist_from_side
		button_size = (self.button_width, button_height)

		for i, inst_set in enumerate(INSTRUMENT_SETS):
			button_y = Window.height - self.button_dist_from_top - (i+1) * (button_height + dist_between_buttons)
			
			button_pos = (button_x, button_y)
			button_state = 'down' if (i==0) else 'normal' # so the first button defaults as down
			button_text = "[size=25sp]" + inst_set + "[/size]" + "\n" + "[size=15sp](" + ", ".join(INSTRUMENT_SETS[inst_set].keys()) + ")[/size]"
			inst_button = ToggleButton(text=button_text, font_size='20sp', markup=True, 
											halign='center', valign='center', id=inst_set,
											pos=button_pos, group='inst_sets', state=button_state,
											size=button_size)
			self.add_game_object(inst_button)
			i += 1

	def which_instrument_set(self):
		"""
		Returns the instrument set that is currently selected on the toggle buttons.
		This is ugly because kivy doesn't have a built in method for figuring out which button is toggled
		"""
		from kivy.uix.togglebutton import ToggleButton as TB
		button_text = next( (t.id for t in TB.get_widgets('inst_sets') if t.state=='down'), None)
		return button_text

	def start_game_callback(self):
		def start_game(button):
			# msg = {'game_info': [b.info() for b in self.band_members]}
			# self.host.send_to_band(msg, 'host')
			print 'starting game'
			inst_set = self.which_instrument_set()
			# self.trigger_event('on_scene_change', scene_name='practice', band_members=msg['game_info'], instrument_set=inst_set)
			self.client.send_action('on_scene_change', scene_name='practice', band_members=self.band_members, instrument_set=inst_set)
		return start_game

	def band_display(self):
		"""
		Sets up the displays for the different band members
		"""
		for i, player in enumerate(self.band_members):
			self.make_user_blurb(i, is_me=(i==0))
			# TODO: Confirm that i==0 thing with the group

	def make_user_blurb(self, user_num, is_me=False):
		"""
		user_num is the user's index in the list of band_members (Host will always have index 0)
		is_me is a flag marked True if this user is me
		"""
		# TODO: Make the is_me flag make the person light up

		# from user_num, compute the offsets (position, size)
		print 'making blurb for user', user_num, self.band_members[user_num]
		start_y_top = Window.height - self.button_dist_from_top
		height = (Window.height - (self.button_dist_from_top + self.button_dist_from_bottom)) / 4.0
		size = Window.width/3.0, height # width should be big enough
		blurb_bottom = start_y_top - size[1] * (user_num+1)
		blurb_top = start_y_top - size[1] * user_num
		blurb_left = self.button_dist_from_side

		# username_text = "[anchor=left_side][color=8888ff][b][size=80]%s   [/size][/b][/color][anchor=right_side]" % 
		username_text = self.band_members[user_num]['username']
		# ip_text = "[anchor=left_side][color=668822][b][size=10]%s[/size][/b][/color][anchor=right_side]" 
		ip_text = self.band_members[user_num]['addr_str']
		
		print username_text

		display_text = '%s : %s' % (username_text, ip_text)
		username_label = TextObject(text=display_text, font_size=40)
		pos=(blurb_left, blurb_bottom)
		self.add_game_object(username_label)

		username_box = RectOutlineSprite(size=size, color=(0.3,0.6,0.8), width=2)
		username_box.position = (100, 100)
		username_label.add_graphic(username_box)
		# self.user_labels.append()
		
		
	def on_update(self):
		pass
		# REMOVE THIS
		# Changed it so you don't have to keep looping on this

		# if self.last_band_member_index < len(self.band_members):
		# 	for i in range(self.last_band_member_index, len(self.band_members)):
		# 		self.make_user_blurb(i, is_me=False)
		
		# TODO: check if new members joined and add them to the view as they join

		# self.waiting_room_label.set_pos((50, Window.height - 200))
		# self.start_game_button.pos = (Window.width * 0.7, Window.height - 200)
		

def build_scene(**kwargs):
	return WaitingRoom(**kwargs)