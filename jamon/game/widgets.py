from game import GameObject

from kivy.uix.textinput import TextInput as _TextInput
from kivy.uix.button import Button as _Button

class Button(GameObject):
	def __init__(self, text, font_size=14):
		super(Button, self).__init__()
		self.widget = _Button(text=text, font_size=font_size)
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
	def __init__(self, text, multiline=True, font_size=14):
		super(TextBox, self).__init__()
		self.widget = _TextInput(text=text, 
								multiline=multiline,
								font_size=font_size)

		self.add_widget(self.widget)
