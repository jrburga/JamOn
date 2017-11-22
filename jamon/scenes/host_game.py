from jamon.game.game import Scene, GameObject

scene = Scene('host_game')

class HostGame(Scene):
	def __init__(self, *kwargs):
		print self.base_widget.game_object.server_object.get_ip_address()

def build_scene(*kwargs):
	return HostGame(*kwargs)