from jamon.game.game import Scene, GameObject
from jamon.game.player import Player
from jamon.game.session import Session

# default music settings
tempo = 120
bars = 1
divs = 4

insts = ['piano', 'drums']*2

class Practice(Scene):
	def __init__(self, band_members, **kwargs):
		super(Practice, self).__init__(**kwargs)
		server_obj = self.base_widget.game_state.server_object
		print band_members
		players = []
		# for bm, band_member in band_members.items()
		for i, bm in enumerate(band_members):
			is_me = bm['ip'] == server_obj.ip or (bm['ip'] == '0' and server_obj.is_host)
			print bm['ip'], server_obj.ip
			players.append(Player(server_obj,
								  bm['username'], 
								  is_me,
								  bars,
								  tempo,
								  i,
								  inst=insts[i]))
		self.add(Session(tempo, bars, divs, players))
		self.add_event_listener('on_key_down', self.change_scene)

	def change_scene(self, s, event):
		if event.keycode[1] == '1':
			self.trigger_event('on_scene_change', scene_name='perform')

print Practice.scene_events
def build_scene(**kwargs):
	return Practice(**kwargs)