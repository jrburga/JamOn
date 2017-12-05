# Scene for when player has clicked join_game and successfully joins

from jamon.game.game import Scene, GameObject
from urllib2 import urlopen
from jamon.game.components.graphics import *
from jamon.game.widgets import *
from kivy.core.window import Window
from jamon.game.text import TextObject

import json


USER_BLURB_SIZE = (800, 150)

class WaitingRoom(Scene):
	def __init__(self, **kwargs):
		super(WaitingRoom, self).__init__(**kwargs)
		self.is_host = kwargs['is_host']

		if self.is_host:
			self.host = self.base_widget.game_state.server_object

			# Trigger host search for other players
			self.host.find_other_players()

		self.band_members = self.base_widget.game_state.server_object.band_members
		self.my_ip = urlopen('http://ip.42.pl/raw').read()
		print self.my_ip

		self.general_display()
		self.band_display()


	def general_display(self):
		"""
		All of the non-player-specific display will be handled here
		"""
		# I apologize for this shitshow below... I'm trying to fix this label thing and I'll have to get to it later -Tim
		self.waiting_room_label_pos = (100, Window.height - 200)
		self.waiting_room_label = TextObject(text="[anchor=left_side][color=ff8888][b]Waiting Room[/b][/color][anchor=right_side]", 
									   font_size=100, markup=True, halign='left', valign='bottom',
									   pos=self.waiting_room_label_pos)

		self.add_game_object(self.waiting_room_label)
		self.start_game_button_pos = (Window.width * 0.7, Window.height - 200)
		if self.is_host:
			# To let host start the game
			self.start_game_button = Button(text="  Start Game  ", font_size='20sp', markup=True, 
											halign='center', valign='top',
									   		pos=self.start_game_button_pos,
			              			   		size=(Window.width * 0.25, Window.height * 0.125))
		print Window.width, Window.height
		# Todo: callback for start game @jake

		self.start_game_button.bind(self.start_game_callback())
		self.add_game_object(self.start_game_button)

	def start_game_callback(self):
		def start_game(button):
			msg = {'game_info': [b.info() for b in self.band_members]}
			self.host.send_to_band(msg, 'host')
			self.trigger_event('on_scene_change', scene_name='practice', band_members=msg['game_info'])
		return start_game

	def band_display(self):
		"""
		Sets up the displays for the different band members
		"""
		print self.band_members
		for i, player in enumerate(self.band_members):
			self.make_user_blurb(i, is_me=(i==0))
			# TODO: Confirm that i==0 thing with the group

	def make_user_blurb(self, user_num, is_me=False):
		"""
		user_num is the user's index in the list of band_members (Host will always have index 0)
		is_me is a flag marked True if this user is me
		"""
		# from user_num, compute the offsets (position, size)
		start_y_top = Window.height - 250
		size = USER_BLURB_SIZE

		blurb_bottom = start_y_top - size[1] * (user_num+1)
		blurb_top = start_y_top - size[1] * user_num
		blurb_left = 50


		# Username label will have height 150 (make text size accordingly?)
		username_label_bottom = blurb_bottom + 50
		username_text = "[anchor=left_side][color=8888ff][b]%s[/b][/color][anchor=right_side]" % self.band_members[user_num].username
		username_label = TextObject(text=username_text, 
									   font_size=80, markup=True, halign='left', valign='bottom',
									   pos=(blurb_left, username_label_bottom))
		
		ip_text = "[anchor=left_side][color=668822][b]%s[/b][/color][anchor=right_side]" % self.band_members[user_num].addr_str

		ip_label = TextObject(text=ip_text, font_size=50, markup=True, halign='left', valign='bottom',
								pos = (blurb_left, blurb_bottom + 10))

		username_box = StaticRect(size=USER_BLURB_SIZE, color=(0.3,0.6,0.8), pos=(blurb_left, blurb_bottom))

		self.add_graphic(username_box)
		self.add_game_object(ip_label)
		self.add_game_object(username_label)
		# self.user_labels.append()
		
		
	def on_update(self):
		
		pass
		# TODO: check if new members joined and add them to the view as they join

		# self.waiting_room_label.set_pos((50, Window.height - 200))
		# self.start_game_button.pos = (Window.width * 0.7, Window.height - 200)
		

def build_scene(**kwargs):
	return WaitingRoom(**kwargs)