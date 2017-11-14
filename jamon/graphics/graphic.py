import sys
sys.path.append('..')

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Ellipse
from common.gfxutil import CEllipse, Color

class Graphic(InstructionGroup):
	def __init__(self, shape, color):
		super(Graphic, self).__init__()
		self.color = Color(rgb=color)
		self.shape = shape()

		self.add(self.color)
		self.add(self.shape)

class EllipseGraphic(Graphic):
	def __init__(self, size, color):
		super(EllipseGraphic, self).__init__(CEllipse, color)
		self.shape.csize = size

class CircleGraphic(Graphic):
	def __init__(self, radius, color):
		super(CircleGraphic, self).__init__(CEllipse, color)