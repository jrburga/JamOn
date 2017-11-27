# Scene for when player has clicked join_game and successfully joins

from jamon.game.game import Scene, GameObject
from urllib2 import urlopen

class WaitingRoom(Scene):
	def __init__(self, **kwargs):
		super(HostGame, self).__init__(**kwargs)
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
									   pos=(Window.width * 0.5, Window.height * 0.4),
			              			   text_size=(Window.width, Window.height))

		self.add_game_object(self.waiting_room_label)

		


def build_scene(**kwargs):
	return WaitingRoom(**kwargs)

