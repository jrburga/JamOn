from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import PushMatrix, PopMatrix
from kivy.graphics import Scale, Rotate, Translate
from kivy.graphics import Ellipse, Rectangle, Color, Line
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel

from jamon.game.common.gfxutil import KFAnim

from kivy.properties import BooleanProperty


# PASTEL COLORSET
RED 	= tuple([0.8 * x for x in [1.0, 0.701960784, 0.729411765]])
ORANGE 	= tuple([0.8 * x for x in [1.0, 0.823529412, 0.701960784]])
YELLOW 	= tuple([1.0 * x for x in [1.0, 0.97254902, 0.701960784]])
BRIGHT_GREEN = tuple([0.9 * x for x in [0.729411765, 1.0, 0.701960784]])
GREEN  	= tuple([0.8 * x for x in [0.729411765, 1.0, 0.701960784]])
DARK_GREEN  = tuple([0.7 * x for x in [0.729411765, 1.0, 0.701960784]])

BLUE 	= tuple([0.9 * x for x in [0.729411765, 0.882352941, 1.0]])
DARK_BLUE = tuple([0.7 * x for x in [0.729411765, 0.882352941, 1.0]])

GRAY 	= (0.9, 0.9, 0.9)
DARK_GRAY = (.75, .75, .75)
DARKER_GRAY = (0.6, 0.6, 0.6)

def hilo(color):
	a, b, c = color
	if c < b: b, c = c, b
	if b < a: a, b = b, a
	if c < b: b, c = c, b
	return a + c

def invert_color(color):
	k = hilo(color)
	return tuple(list(tuple(k - u for u in color)))

# def invert_color(color):
# 	brightness = color[0] **2 + color[1] ** 2 + color[2] ** 2

# 	color[1]
# 	return tuple([1 - c for c in list(color)])


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
		if sprite in self._objects:
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

class RectOutlineSprite(Sprite):
	def __init__(self, size, color, width=2):
		w, h = size
		super(RectOutlineSprite, self).__init__(Line(points=[0,0,w,0,w,h-width,0,h-width,0,0], width=width), color)

class GradientRectSprite(Sprite):
	def __init__(self, size, color_1, color_2, dir='vertical'):
		  texture = Texture.create(size=size, colorfmt="rgb")
		  if dir=='vertical':
			p_size = size[1]
			width = size[0]
			buf = []
			for x in range(p_size):
				for _ in range(width):
					for i in range(3):
						buf.append(int(color_1[i]*255-x*(color_1[i]-color_2[i])*255/p_size))
			buf = b''.join(map(chr, buf))
			texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
			super(GradientRectSprite, self).__init__(Rectangle(texture=texture, size=size), (1,1,1))


class TextSprite(Sprite):
	def __init__(self, text, pos=(0, 0), color=(1,1,1), font_size=20, stretch=(1,1), **text_kwargs):
		text = MarkupLabel(text=text, font_size=font_size, **text_kwargs)
		text.refresh()
		# Create rectangle object for the text
		new_size = (text.size[0]*stretch[0], text.size[1]*stretch[1])
		rect = Rectangle(size=new_size, pos=pos, texture=text.texture)
		super(TextSprite, self).__init__(rect, color)

class ImageSprite(Sprite):
	def __init__(self, fname, color=(1,1,1), **kwargs):
		super(ImageSprite, self).__init__(Rectangle(source='images/'+fname, **kwargs), color)

