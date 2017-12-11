from jamon.game.game import Scene, GameObject
from jamon.game.player import Player
from jamon.game.session import Session

# default music settings
tempo = 120
bars = 4
divs = 4

class Practice(Scene):
	def __init__(self, **kwargs):
		super(Practice, self).__init__(**kwargs)
		self.inst_set = kwargs['instrument_set']



	def on_load(self):
		band_members = self.client.get_band_members()
		print 'band_members', band_members
		print '============'
		other_members = []
		for band_member in band_members:
			if band_member['id'] == self.client.id:
				continue
			other_members.append(band_member)
		self.add(Session(other_members, tempo, bars, divs, self.inst_set))
		self.add_event_listener('on_key_down', self.change_scene)

	def change_scene(self, s, event):
		if event.keycode[1] == '1':
			self.trigger_event('on_scene_change', scene_name='perform')

# print Practice.scene_events
def build_scene(**kwargs):
	print 'building scene', kwargs
	return Practice(**kwargs)