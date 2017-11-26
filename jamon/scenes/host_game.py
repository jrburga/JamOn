from jamon.game.game import Scene, GameObject
from urllib2 import urlopen

class HostGame(Scene):
	def __init__(self, **kwargs):
		super(HostGame, self).__init__(**kwargs)
		self.host = self.base_widget.game_state.server_object

		# Trigger host search for other players
		self.host.find_other_players()
		self.my_ip = urlopen('http://ip.42.pl/raw').read()
		
		print self.my_ip

def build_scene(**kwargs):
	return HostGame(**kwargs)