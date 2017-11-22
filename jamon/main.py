from game.common.core import *
from game.common.audio import Audio

from scenes import scenes
import numpy as np

class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()
		self.audio = Audio(2)

		self.scenes = {scene.name: scene for scene in scenes}
		self.scene = None

		self.game_state = GameState()
		
		start_scene = 'main_menu'
		for scene in scenes:
			if scene.name == start_scene:
				self.load_new_scene(scene)
				break
		else:
			self.load_new_scene(scenes[0])

	def unload_current_scene(self):
		if self.scene == None: return
		self.scene.base_widget = None
		self.canvas.remove(self.scene._transform)
		self.audio.set_generator(None)
		for widget in self.scene.widgets:
			self.remove_widget(widget)

	def load_new_scene(self, scene):
		self.unload_current_scene()
		self.scene = scene
		self.scene.base_widget = self
		self.audio.set_generator(scene._mixer)
		self.canvas.add(scene._transform)
		print 'loading scene', scene.widgets
		for widget in self.scene.widgets:
			self.add_widget(widget)

	def on_key_down(self, keycode, modifiers):
		self.scene.trigger_event('on_key_down', 
								  keycode=keycode, 
								  modifiers=modifiers)

	def on_key_up(self, keycode):
		self.scene.trigger_event('on_key_up',
								 keycode=keycode)
		
	def on_touch_down(self, touch):
		super(MainWidget, self).on_touch_down(touch)
		self.scene.trigger_event('on_touch_down',
								  touch=touch)

	def on_touch_up(self, touch):
		super(MainWidget, self).on_touch_up(touch)
		self.scene.trigger_event('on_touch_up',
								  touch=touch)

	def on_touch_move(self, touch):
		super(MainWidget, self).on_touch_move(touch)
		self.scene.trigger_event('on_touch_move',
								  touch=touch)

	def on_scene_change(self, event):
		self.load_new_scene(self.scenes[event.scene_name])
	
	def on_server_request(self, event):
		print event.server_type

		if event.server_type == "host_game":
			self.game_state.server_object = Host()
		elif event.server_type == "join_game":
			self.game_state.server_object = Host()


	def on_update(self):
		self.scene._on_update()
		self.audio.on_update()


class GameState(object):
	def __init__(self):
		self.username = "Guest_" + str(np.random.randint(1000000))
		self.server_object = None    # Will be a server object of the subclass Host or Guest
        








