from game import GameObject

from kivy.uix.textinput import TextInput as _TextInput
from kivy.uix.button import Button as _Button

class Button(GameObject):
	def __init__(self, **kwargs):
		super(Button, self).__init__()
		self.widget = _Button(**kwargs)
		self.widget.bind(on_press=self._on_press)
		self.add_widget(self.widget)

	def _on_press(self, instance):
		self.on_press()

	def on_press(self):
		print 'go callback'
		# self.trigger_event()

	@property
	def text(self):
		return self.widget.text

class TextBox(GameObject):
	def __init__(self, **kwargs):
		super(TextBox, self).__init__()
		self.widget = _TextInput(**kwargs)

		self.add_widget(self.widget)
