from jamon.game.game import Scene, GameObject
from jamon.game.player import Player
from jamon.game.session import Session

# default music settings
tempo = 120
bars = 4
divs = 4

insts = ['piano', 'vibraphone', 'guitar']*2

class Practice(Scene):
	def __init__(self, **kwargs):
		super(Practice, self).__init__(**kwargs)

	def on_load(self):
		self.add(Session(tempo, bars, divs))
		self.add_event_listener('on_key_down', self.change_scene)

	def change_scene(self, s, event):
		if event.keycode[1] == '1':
			self.trigger_event('on_scene_change', scene_name='perform')

# print Practice.scene_events
def build_scene(**kwargs):
	print 'building scene', kwargs
	return Practice(**kwargs)