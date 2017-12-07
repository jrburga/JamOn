from game import GameObject
from components.graphics import TextSprite


class TextObject(GameObject):

	def __init__(self, text, **kwargs):
		super(TextObject, self).__init__()

		self.done = False
		self.text = text
		self.add_graphic(TextSprite(self.text, **kwargs))
		# self.kwargs = kwargs


	def draw(self, stretch):
		pass
		# self.stretch = stretch
		# self.sprite = TextSprite(self.text, stretch = stretch, **self.kwargs)
		# self.add_graphic(self.sprite)

	def on_update(self):
		if self.done:
			return

		if self._parent is not None:
			self.done = True
			x1, y1 = (1,1)
			parent = self._parent
			while parent is not None:
				x2, y2, _ = parent.scale.xyz
				x1 *= x2
				y1 *= y2
				parent = parent._parent
			stretch = (1./x1, 1./y1)
			self.draw(stretch)

