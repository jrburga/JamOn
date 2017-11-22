from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import PushMatrix, PopMatrix
from kivy.graphics import Scale, Rotate, Translate
from kivy.graphics import Ellipse, Rectangle, Color
from kivy.core.image import Image

from jamon.game.common.gfxutil import KFAnim

class Transform(InstructionGroup):
	def __init__(self, graphics):
		super(Transform, self).__init__()
		self.position = Translate()
		self.rotation = Rotate()
		self.scale = Scale()
		self.add(PushMatrix())
		self.add(self.position)
		self.add(self.rotation)
		self.add(self.scale)
		self.add(graphics)
		self.add(PopMatrix())

class Graphics(InstructionGroup):
	def __init__(self):
		super(Graphics, self).__init__()
		self._objects = set()

	def add(self, sprite):
		super(Graphics, self).add(sprite)
		self._objects.add(sprite)

	def remove(self, sprite):
		super(Graphics, self).remove(sprite)
		self._objects.remove(sprite)

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
		# self.center = 
		self.add(self.color)
		self.add(self.texture)

	@property
	def size(self):
		return self.texture.size

	@size.setter
	def size(self, new_size):
		self.texture.size = new_size

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
		print "center set"
		cx, cy = new_center
		self.position = (cx - self.size[0]/2, cy - self.size[1]/2)

	@property
	def size(self):
		return self.texture.size

	def on_update(self, dt):
		return True

class EllipseSprite(Sprite):
	def __init__(self, size, color):
		super(EllipseSprite, self).__init__(Ellipse(size=size), color)

class CircleSprite(Sprite):
	def __init__(self, radius, color):
		super(CircleSprite, self).__init__(Ellipse(size=(radius/2, radius/2)), color)

class RectSprite(Sprite):
	def __init__(self, size, color):
		super(RectSprite, self).__init__(Rectangle(size=size), color)

