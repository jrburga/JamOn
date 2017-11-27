from jamon.game.game import Scene, GameObject
from jamon.game.session import Session

class Practice(Scene):
	def __init__(self, **kwargs):
		super(Practice, self).__init__(**kwargs)
		self.add(Session())
		self.add_event_listener('on_key_down', self.change_scene)

	def change_scene(self, s, event):
		if event.keycode[1] == '1':
			self.trigger_event('on_scene_change', scene_name='perform')

print Practice.scene_events
def build_scene(**kwargs):
	return Practice(**kwargs)