from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from kivy.core.window import Window
from server.server_parties import PORT
from thread import *

class JoinGame(Scene):
	def __init__(self, **kwargs):
		super(JoinGame, self).__init__(**kwargs)

		self.client = self.base_widget.client_obj
		self.add(self.client)
		print kwargs
		self.display()
		self.attempting_connection = False

	def display(self):
		"""
		Builds the graphics for the scene
		"""

		self.ip_label = Label(text="[anchor=left_side][color=ff8888]Enter the IP of the host below[/color][anchor=right_side]", 
						   font_size='20sp', markup=True, halign='center', valign='top',
						   pos=(Window.width * 0.5, Window.height * 0.4),
              			   text_size=(Window.width, Window.height))
		self.failure_label = Label(text = "", valign='top', font_size='20sp', halign='center',
			                pos=(Window.width * 0.5, Window.height * 0.8),
			                text_size=(Window.width, Window.height))

		self.text_box = TextBox(pos=(Window.width * 0.25, Window.height * 0.4), multiline=False,
								on_text_validate=self.attempt_connection, size=(Window.width * 0.5, Window.height * 0.1))
		
		self.add_game_object(self.text_box)
		self.add_game_object(self.failure_label)
		self.add_game_object(self.ip_label)

	def attempt_connection(self, *args):
		"""
		For attempting to connect
		"""
		if self.attempting_connection:
			print "Already attemping to connect. Chill out dude."
			return 
		print "Attempting to connect to", self.text_box.text
		self.attempting_connection = True

		start_new_thread(self._attempt_connection_thread, ())

	def _attempt_connection_thread(self, *args):
		"""
		Actually attempts the connection. Should be called in another thread
		"""
		ip = self.text_box.text
		port = PORT

		# (2a) while connecting, display a "cancel" button or something
		# TODO

		# (2b) try to connect with the Guest's connect function 
		# self.guest.set_host_ip(ip)
		
		self.client.connect(ip)

		# (3) if success, change scene to band scene
		self.attempting_connection = False
		print "Connection successful!"

		# self.guest.send_to_band({'yo':True}, host_only=True)

def build_scene(**kwargs):
	return JoinGame(**kwargs)