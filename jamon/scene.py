from common.gfxutil import AnimGroup
from common.mixer import Mixer



from collections import deque, defaultdict

class Event(object):
	def __init__(self, event_type, **kwargs):
		self.type = event_type
		self.__dict__.update(kwargs)

class Scene(object):
	def __init__(self):
		self._game_objects = set()
		self._event_listeners = defaultdict(lambda : [])

		self.graphics = AnimGroup()
		self.mixer = Mixer()

		self.events = deque()

	def add_event_listener(self, event, callback):
		self._event_listeners[event].append(callback)

	def trigger_event(self, event_type, **kwargs):
		event = Event(event_type, **kwargs)
		self.events.append(event)

	def _handle_events(self):
		while self.events:
			event = self.events.pop()
			for callback in self._event_listeners[event.type]:
				callback(scene, event)


	def add_game_object(self, game_object):
		self._game_objects.add(game_object)

	def remove_game_object(self, game_object):
		self._game_objects.remove(game_object)

	def on_update(self):
		self.graphics.on_update()

class GameObject(object):
	'''
	Game Objects can contain each other 
	(like HTML divs, or something)
	'''
	def __init__(self):
		self.graphic = None
		self.generator = None
		self.parent = None
		self.children = []