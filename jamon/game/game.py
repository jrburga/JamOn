from common.mixer import Mixer
from components.graphics import Graphics, Transform

from kivy.clock import Clock as kivyClock
from collections import deque, defaultdict


class Event(object):
	def __init__(self, event_type, **kwargs):
		self.type = event_type
		self.__dict__.update(kwargs)

	@property
	def __kwargs__(self):
		d = dict(self.__dict__)
		del d['type']
		return d

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

class GameObject(object):
	'''
	Game Objects can contain each other 
	(like HTML divs, or something)
	'''
	def __init__(self):
		super(GameObject, self).__init__()

		self._graphics = Graphics()
		self._transform = Transform(self._graphics)
		self._mixer = Mixer()
		self._parent = None
		self._game_objects = set()
		self._widgets = set()
		self._event_listeners = defaultdict(lambda: [])

		self.updating = False
		self.to_add = []

	@property
	def widgets(self):
		widgets = self._widgets.copy()
		for go in self._game_objects:
			widgets.update(go.widgets)
		return widgets
		
	def add_widget(self, widget):
		self._widgets.add(widget)
		# self._add_widget(widget)

	def get_abs_pos(self):
		x = self.position.x
		y = self.position.y
		x *= self.scale.x
		y *= self.scale.y
		parent = self._parent
		while parent is not None:
			xp = parent.position.x
			yp = parent.position.y
			x += xp * parent.scale.x
			y += yp * parent.scale.y
			parent = parent._parent

		return x,y

	def on_add(self):
		pass

	@property
	def position(self):
		return self._transform.position

	@position.setter
	def position(self, new_pos):
		self._transform.position.xy = new_pos
		for widget in self._widgets:
			widget.pos = new_pos

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
		self._graphics.add(graphic)

	def remove_graphic(self, graphic):
		self._graphics.remove(graphic)

	def add_generator(self, generator):
		self._mixer.add(generator)

	def remove_generator(self, generator):
		self._mixer.remove(generator)

	def add(self, *game_objects):
		for go in game_objects:
			if self.updating:
				self.to_add.append(go)
			else:
				self.add_game_object(go)
				go.on_add()

	def add_game_object(self, game_object):
		# self.add_widget(game_object)
		# assert game_object._parent == None, 'game object already has parent'
		if game_object._parent:
			game_object._parent.remove(game_object)
		game_object._parent = self
		self._game_objects.add(game_object)
		self._graphics.add(game_object._transform)
		self._mixer.add(game_object._mixer)

	def remove(self, *game_objects):
		for go in game_objects:
			self.remove_game_object(go)

	def remove_game_object(self, game_object):
		# pass
		if game_object._parent != self: return
		game_object._parent = None
		self._game_objects.remove(game_object)
		self._graphics.remove(game_object._transform)
		self._mixer.remove(game_object._mixer)

	def add_event_listener(self, event, callback):
		self._event_listeners[event].append(callback)

	def trigger_event(self, event_type, **kwargs):
		assert self._parent != None, 'Game Object needs to be attached to a scene.\nEvent Lost to the void'
		self._parent.trigger_event(event_type, **kwargs)

	def _handle_event(self, event):
		if hasattr(self, event.type):
			getattr(self, event.type)(event)

		for callback in self._event_listeners[event.type]:
			callback(self, event)

		for go in self._game_objects:
			go._handle_event(event)

	def _on_update(self):
		self.updating = True
		self.on_update()
		dt = kivyClock.frametime
		self._graphics.on_update(dt)
		for go in self._game_objects:
			go._on_update()
		self.updating = False
		for go in self.to_add:
			self.add(go)
		self.to_add = []

	def on_update(self):
		pass

	def on_add(self):
		pass

class Scene(GameObject):
	name = None
	scene_events = ['on_scene_change', 'on_server_request']
	def __init__(self, base_widget, **kwargs):
		super(Scene, self).__init__()
		self.base_widget = base_widget
		self._events = deque()
		self._events = []

	def _add_widget(self, widget):
		return
		assert self.base_widget, 'Scene needs base widget to attach widget'
		self.base_widget.add_widget(widget)

	def next_scene(self):
		new_scene = self._new_scene
		self._new_scene = None
		return new_scene

	def trigger_event(self, event_type, **kwargs):
		self._events.append(Event(event_type, **kwargs))

	def _handle_event(self, event):
		super(Scene, self)._handle_event(event)
		if event.type in self.scene_events:
			if self.base_widget:
				getattr(self.base_widget, event.type)(event)

	def _on_update(self):

		while self._events:
			self._handle_event(self._events.pop(0))
		super(Scene, self)._on_update()

	def on_update(self):
		pass


