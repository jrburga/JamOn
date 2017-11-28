# Scene for when player has clicked join_game and successfully joins

from jamon.game.game import Scene, GameObject
from urllib2 import urlopen
from jamon.game.components.graphics import *
from jamon.game.widgets import *

USER_BLURB_SIZE = (400, 250)

class WaitingRoom(Scene):
	def __init__(self, **kwargs):
		super(WaitingRoom, self).__init__(**kwargs)
		self.is_host = kwargs['is_host']

		if self.is_host:
			self.host = self.base_widget.game_state.server_object

			# Trigger host search for other players
			self.host.find_other_players()

		self.my_ip = urlopen('http://ip.42.pl/raw').read()
		print self.my_ip

	def general_display(self):
		"""
		All of the non-player-specific display will be handled here
		"""

		self.waiting_room_label = Label(text="[anchor=left_side][color=ff8888][b]Waiting Room[/b][/color][anchor=right_side]", 
									   font_size='20sp', markup=True, halign='left', valign='top',
									   pos=(600, 200),
			              			   text_size=(Window.width, Window.height))

		self.add_game_object(self.waiting_room_label)
		
		# Let host start the game
		if self.is_host:
			self.start_game_button = Button(text="Start Game", font_size='20sp', markup=True, 
											halign='center', valign='top',
									   		pos=(Window.width * 0.7, Window.height * 0.2),
			              			   		size=(200, 150))

		# Todo: callback for start game
		# self.start_game_button.bind()
		self.add_game_object(self.start_game_button)


	def make_user_blurb(self, user_num, is_me=False):
		"""
		user_num is the user's index in the list of band_members (Host will always have index 0)
		is_me is a flag marked True if this user is me
		"""
		# from user_num, compute the offsets (position, size)
		# pos is top left pos (left_x,top_y)
		size = USER_BLURB_SIZE
		
		# = TextSprite()


def build_scene(**kwargs):
	return WaitingRoom(**kwargs)

