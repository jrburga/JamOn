from jamon.game.game import Scene, GameObject

class JoinGame(Scene):
	def __init__(self, **kwargs):
		super(JoinGame, self).__init__(**kwargs)
		print kwargs

def build_scene(**kwargs):
	return JoinGame(**kwargs)