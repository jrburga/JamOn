from game.game import Event
from game.common.core import *
from game.common.audio import Audio
from game.networking import ClientObject
# from server.server_parties import *
from scenes import scenes
import numpy as np

from server import Client, Server, PUBLIC

class MainWidget(BaseWidget):
	def __init__(self, argv):
		super(MainWidget, self).__init__()

		self.audio = Audio(2)

		self.server = Server()
		self.client = Client()
		self.client_obj = ClientObject(self.client, username=None)
		self.band_members = []

		self.scenes = scenes
		self.scene = None

		start_scene = 'main_menu'
		args = []
		kwargs = {}

		if len(argv) > 1:
			if argv[1] == 'practice':
				start_scene = 'practice'
				kwargs = {'band_members': []}
		
		
		if start_scene:
			self.load_new_scene(start_scene, **kwargs)
		else:
			self.load_new_scene(scenes.keys()[0], **kwargs)

	def unload_current_scene(self):
		if self.scene == None: return
		self.scene.base_widget = None
		self.canvas.remove(self.scene._transform)
		self.audio.set_generator(None)
		for widget in self.scene.widgets:
			self.remove_widget(widget)

	def load_new_scene(self, scene_name, **kwargs):
		self.unload_current_scene()
		self.scene = self.scenes[scene_name](base_widget=self, **kwargs)
		self.audio.set_generator(self.scene._mixer)
		self.canvas.add(self.scene._transform)
		for widget in self.scene.widgets:
			self.add_widget(widget)

	def on_key_down(self, keycode, modifiers):
		self.scene._handle_event(Event('on_key_down', 
							  			keycode=keycode, 
							  			modifiers=modifiers))

	def on_key_up(self, keycode):
		self.scene._handle_event(Event('on_key_up',
								 		keycode=keycode))
		
	def on_touch_down(self, touch):
		super(MainWidget, self).on_touch_down(touch)
		self.scene._handle_event(Event('on_touch_down',
								  		touch=touch))

	def on_touch_up(self, touch):
		super(MainWidget, self).on_touch_up(touch)
		self.scene._handle_event(Event('on_touch_up',
								  		touch=touch))

	def on_touch_move(self, touch):
		super(MainWidget, self).on_touch_move(touch)
		self.scene._handle_event(Event('on_touch_move',
								  		touch=touch))

	def on_scene_change(self, event):
		print event.__kwargs__
		self.load_new_scene(**event.__kwargs__)
	
	def on_server_request(self, event):
		if event.server_type == "host_game":
			print 'starting server'
			self.server.start()
			print 'host connection to server'
			self.client.connect(PUBLIC)
			print 'host connected to server'

		elif event.server_type == "join_game":
			self.server = None

	def on_update(self):
		self.scene._on_update()
		self.audio.on_update()







