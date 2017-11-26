from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from kivy.core.window import Window
from server.server_parties import PORT

class JoinGame(Scene):
	def __init__(self, **kwargs):
		super(JoinGame, self).__init__(**kwargs)

		self.guest = self.base_widget.game_state.server_object
		print kwargs
		self.display()

	def display(self):
		"""
		Builds the graphics for the scene
		"""

		self.ip_label = Label(text="[anchor=left_side][color=ff8888]Enter the IP of the host below[/color][anchor=right_side]", 
						   font_size='20sp', markup=True, halign='center', valign='top',
						   pos=(Window.width * 0.5, Window.height * 0.4),
              			   text_size=(Window.width, Window.height))
		self.failure_label = Label(text = "", valign='top', font_size='20sp', halign='center'
			                pos=(Window.width * 0.5, Window.height * 0.8),
			                text_size=(Window.width, Window.height))

		self.text_box = TextBox(pos=(Window.width * 0.5, Window.height * 0.4), multiline=False,
								on_text_validate=self.attempt_connection)
		
		# self.text_box = TextBox()

		self.add_game_object(self.text_box)
		self.add_game_object(self.failure_label)
		self.add_game_object(self.ip_label)


	def attempt_connection(self):
		"""
		For attempting to connect
		"""
		self.attempting_connection = True
		# (1) Confirm IP address is a valid IP
		try:
			socket.inet_aton(addr)
		except:
			self.failure_label.text = "Not a valid IP, please try again"
			self.attempting_connection = False
			return

		ip = self.text_box.text
		port = PORT

		# (2a) while connecting, display a "cancel" button or something
		# TODO

		# (2b) try to connect with the Guest's connect function 
		self.guest.set_host_ip(ip)
		try:
			self.guest.connect_to_host(timeout=10)
		except Exception as e:
			self.failure_label.text = "Unable to connect. Please try again"
			self.attempting_connection = False
			return

		# (3) if success, change scene to band scene
		self.attempting_connection = False

def build_scene(**kwargs):
	return JoinGame(**kwargs)