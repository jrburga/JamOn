from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Ellipse, Rectangle, Color, Scale, Rotate, Translate
from kivy.core.image import Image

from ..common.gfxutil import AnimGroup

class Graphics(InstructionGroup):
	def __init__(self):
		super(Graphics, self).__init__()
		self.rotation = Rotate()
		self.position = Translate()
		self.scale = Scale()
		self._objects = set()

		self.add(self.position)
		self.add(self.rotation)
		self.add(self.scale)

	def add(self, sprite):
		super(Graphics, self).add(sprite)
		self._objects.add(sprite)

	def on_update(self, dt):
		kill_list = set()
		for obj in self._objects:
			if hasattr(obj, 'on_update') and not obj.on_update(dt):
				kill_list.add(obj)

		for obj in kill_list:
			self._objects.remove(obj)
			self.remove(obj)
		return True

class Sprite(InstructionGroup):
	def __init__(self, texture, color):
		super(Sprite, self).__init__()
		self.color = Color(rgb=color)
		self.texture = texture

		self.add(self.color)
		self.add(self.texture)

	@property
	def size(self):
		return self.texture.size

	@property
	def position(self):
		return self.texture.pos

	@position.setter
	def position(self, new_pos):
		self.texture.pos = new_pos

	@property
	def center(self):
		cx = self.position[0] + self.size[0]/2
		cy = self.position[1] + self.size[1]/2
		return (cx, cy)

	@center.setter
	def center(self, new_center):
		cx, cy = new_center
		self.position = (cx - self.size[0]/2, cy - self.size[1]/2)

	@property
	def size(self):
		return self.texture.size

	def on_update(self, dt):
		return True

class EllipseSprite(Sprite):
	def __init__(self, size, color):
		super(EllipseSprite, self).__init__(Ellipse(), color)
		self.texture.csize = size

class CircleSprite(Sprite):
	def __init__(self, radius, color):
		super(CircleSprite, self).__init__(Ellipse(), color)
		self.texture.size = (radius, radius)

class RectSprite(Sprite):
	def __init__(self, size, color):
		super(RectSprite, self).__init__(Rectangle(), color)
		self.texture.size = size