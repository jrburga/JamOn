class Event(object):
	pass

class Game(object):
	pass

class Scene(object):
	def __init__(self):
		self._game_objects = set()
		self._event_handlers = {}

	def add_event_handler(self, event, callback):
		self._event_handlers[event].append(callback)

	def _handle_events(self, events):
		for event in events:
			for callback in self._event_handlers[event.type]:
				callback(self, event)

	def add_game_object(self, game_object):
		self._game_objects.add(game_object)

	def remove_game_object(self, game_object):
		self._game_objects.remove(game_object)

class GameObject(object):
	def __init__(self):
		self._components = set()

	def add_component(self, component):
		self._components.add(component)

	def remove_component(self, component):
		self._components.remove(component)
