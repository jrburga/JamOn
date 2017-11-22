from jamon.game.game import Scene, GameObject

class HostGame(Scene):
	def __init__(self, **kwargs):
		super(HostGame, self).__init__(**kwargs)
		print self.base_widget.game_state.server_object.get_ip_address()

def build_scene(**kwargs):
	return HostGame(**kwargs)