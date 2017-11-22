from jamon.game.game import Scene, GameObject
from jamon.game.session import Session

class Practice(Scene):
	def __init__(self, **kargs):
		super(Practice, self).__init__()
		self.add(Session())

def build_scene(**kwargs):
	return Practice(**kwargs)