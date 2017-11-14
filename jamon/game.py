from common.mixer import Mixer

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Scale, Rotate, Translate

from collections import deque, defaultdict

class Event(object):
	def __init__(self, event_type, **kwargs):
		self.type = event_type
		self.__dict__.update(kwargs)

class Game(object):
	def __init__(self):
		self._scenes = {}
		self._scene = None

	def add_scene(self, scene_name, scene):
		self._scenes[scene_name] = scene

	def set_scene(self, scene_name):
		# Should probably do something to "unmount" the current scene
		self._scene = self._scenes[scene_name]

	@property
	def scene(self):
		return self._scene

class Transform(InstructionGroup):
	def __init__(self):
		super(Transform, self).__init__()
		
		self.rotation = Rotate()
		self.position = Translate()
		self.scale = Scale()

		self.add(self.position)
		self.add(self.rotation)
		self.add(self.scale)

class GameObject(object):
	'''
	Game Objects can contain each other 
	(like HTML divs, or something)
	'''
	def __init__(self):
		self._transform = Transform()
		self._mixer = Mixer()
		self._parent = None
		self._game_objects = set()
		self._event_listeners = defaultdict(lambda: [])

	@property
	def position(self):
		return self._transform.position

	@position.setter
	def position(self, new_pos):
		self._transform.position.x = new_pos[0]
		self._transform.position.y = new_pos[1]

	@property
	def rotation(self):
		return self._transform.rotation

	@rotation.setter
	def rotation(self, new_rotation):
		self._transform.rotation.angle = new_rotation

	@property
	def scale(self):
		return self._transform.scale

	@scale.setter
	def scale(self, new_scale):
		self._transform.scale.x = new_scale
		self._transform.scale.y = new_scale

	def add_graphic(self, graphic):
		self._transform.add(graphic)

	def add_game_object(self, game_object):
		assert game_object._parent == None, 'game object already has parent'
		game_object._parent = self
		self._game_objects.add(game_object)
		self._transform.add(game_object._transform)
		self._mixer.add(game_object._mixer)

	def remove_game_object(self, game_object):
		if game_object._parent != self: return
		game_object._parent = None
		self._game_objects.remove(game_object)
		self._transform.remove(game_object._transform)
		self._mixer.remove(game_object._mixer)

	def add_event_listener(self, event, callback):
		self._event_listeners[event].append(callback)

	def trigger_event(self, event_type, **kwargs):
		assert self._parent != None, 'Game Object needs to be attached to a scene.\nEvent Lost to the void'
		self._parent.trigger_event(event_type, **kwargs)

	def _handle_event(self, event):
		for callback in self._event_listeners[event.type]:
			callback(self, event)

		for go in self._game_objects:
			go._handle_event(event)

	def _on_update(self):
		self.on_update()
		for go in self._game_objects:
			go._on_update()

	def on_update(self):
		pass

class Scene(GameObject):
	def __init__(self):
		super(Scene, self).__init__()
		self._events = deque()

	def trigger_event(self, event_type, **kwargs):
		self._events.append(Event(event_type, **kwargs))

	def _on_update(self):
		while self._events:
			self._handle_event(self._events.pop())
		super(Scene, self)._on_update()

	def on_update(self):
		pass



if __name__ == '__main__':
	scene = Scene()
	game_object  = GameObject()

