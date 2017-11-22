from jamon.game.game import Scene, GameObject



class JoinGame(Scene):
	def __init__(self, *kwargs):
		print args

def build_scene(*kwargs):
	return JoinGame(*kwargs)