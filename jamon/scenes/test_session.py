from jamon.game.game import Scene, GameObject
from jamon.game.player import Player, PlayerRemote
from jamon.game.session import Session

from server.dummy_parties import ServerObject

# default music settings
tempo = 120
bars = 4
divs = 4

class TestSession(Scene):
	def __init__(self, **kwargs):
		super(TestSession, self).__init__(**kwargs)
		self.base_widget.game_state.server_object
		players = [Player(bars, tempo), 
				   PlayerRemote(bars, tempo, num=2, inst='drums')]
		self.add(Session(tempo, bars, divs, players))
		self.add_event_listener('on_key_down', self.change_scene)

	def change_scene(self, s, event):
		if event.keycode[1] == '1':
			self.trigger_event('on_scene_change', scene_name='perform')

def build_scene(**kwargs):
	return TestSession(**kwargs)